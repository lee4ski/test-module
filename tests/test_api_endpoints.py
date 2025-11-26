import pytest
from fastapi import status


@pytest.mark.api
class TestAPIEndpoints:
    """Tests for API endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()

    def test_comparison_index_page(self, client):
        """Test comparison index page loads"""
        response = client.get("/comparison/")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]
        assert "Data Comparison Tool" in response.text

    def test_comparison_results_page(self, client):
        """Test comparison results page loads"""
        response = client.get("/comparison/results")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]
        assert "Comparison Results" in response.text

    def test_compare_api_with_valid_files(self, client, sample_excel_ground_truth, sample_excel_extracted):
        """Test compare API with valid Excel files"""
        files = {
            "ground_truth": ("ground_truth.xlsx", sample_excel_ground_truth, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            "extracted_result": ("extracted.xlsx", sample_excel_extracted, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        }
        
        response = client.post("/comparison/api/compare", files=files)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["success"] is True
        assert "result" in data
        assert data["result"]["total_rows"] > 0
        assert "headers" in data["result"]
        assert "rows" in data["result"]

    def test_compare_api_with_csv_files(self, client, sample_csv_ground_truth, sample_csv_extracted):
        """Test compare API with CSV files"""
        files = {
            "ground_truth": ("ground_truth.csv", sample_csv_ground_truth, "text/csv"),
            "extracted_result": ("extracted.csv", sample_csv_extracted, "text/csv")
        }
        
        response = client.post("/comparison/api/compare", files=files)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["success"] is True
        assert "result" in data

    def test_compare_api_missing_files(self, client):
        """Test compare API with missing files"""
        response = client.post("/comparison/api/compare")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_compare_api_invalid_file(self, client):
        """Test compare API with invalid file format"""
        # Use corrupted Excel file (pandas is very lenient with CSV, so we test with corrupted Excel)
        # Corrupted ZIP structure (Excel files are ZIP archives)
        invalid_content = b"PK\x03\x04" + b"\x00" * 100
        files = {
            "ground_truth": ("invalid.xlsx", invalid_content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            "extracted_result": ("invalid.xlsx", invalid_content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        }
        
        response = client.post("/comparison/api/compare", files=files)
        # The API should handle the error gracefully
        # It may return 200 with error in response, or 400/500
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR, status.HTTP_200_OK]
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            # If 200, should have error in response
            assert not data.get("success", True) or "error" in data or "detail" in data

    def test_compare_api_response_structure(self, client, identical_files):
        """Test that API response has correct structure"""
        gt_file, ext_file = identical_files
        files = {
            "ground_truth": ("gt.xlsx", gt_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            "extracted_result": ("ext.xlsx", ext_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        }
        
        response = client.post("/comparison/api/compare", files=files)
        data = response.json()
        
        assert "success" in data
        assert "result" in data
        result = data["result"]
        
        assert "headers" in result
        assert "rows" in result
        assert "total_rows" in result
        assert "matched_rows" in result
        assert "mismatched_rows" in result
        assert "overall_confidence" in result
        
        # Check row structure
        if len(result["rows"]) > 0:
            row = result["rows"][0]
            assert "row_index" in row
            assert "cells" in row
            
            if len(row["cells"]) > 0:
                cell = row["cells"][0]
                assert "value" in cell
                assert "ground_truth" in cell
                assert "extracted" in cell
                assert "match" in cell
                assert "confidence" in cell

