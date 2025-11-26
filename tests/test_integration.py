import pytest
from fastapi import status
import pandas as pd
import io


@pytest.mark.integration
class TestIntegration:
    """Integration tests for the complete workflow"""

    def test_complete_workflow_excel_files(self, client):
        """Test complete workflow with Excel files"""
        # Create test data
        df1 = pd.DataFrame({
            'Name': ['Test1', 'Test2'],
            'Value': [100, 200]
        })
        df2 = pd.DataFrame({
            'Name': ['Test1', 'Test2'],
            'Value': [100, 200]
        })
        
        buffer1 = io.BytesIO()
        buffer2 = io.BytesIO()
        df1.to_excel(buffer1, index=False, engine='openpyxl')
        df2.to_excel(buffer2, index=False, engine='openpyxl')
        buffer1.seek(0)
        buffer2.seek(0)
        
        # Upload and compare
        files = {
            "ground_truth": ("gt.xlsx", buffer1.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            "extracted_result": ("ext.xlsx", buffer2.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        }
        
        response = client.post("/comparison/api/compare", files=files)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["success"] is True
        assert data["result"]["matched_rows"] == 2

    def test_complete_workflow_csv_files(self, client):
        """Test complete workflow with CSV files"""
        # Create test data
        df1 = pd.DataFrame({
            'Product': ['A', 'B'],
            'Price': [10, 20]
        })
        df2 = pd.DataFrame({
            'Product': ['A', 'B'],
            'Price': [10, 20]
        })
        
        buffer1 = io.BytesIO()
        buffer2 = io.BytesIO()
        df1.to_csv(buffer1, index=False, encoding='utf-8')
        df2.to_csv(buffer2, index=False, encoding='utf-8')
        buffer1.seek(0)
        buffer2.seek(0)
        
        # Upload and compare
        files = {
            "ground_truth": ("gt.csv", buffer1.getvalue(), "text/csv"),
            "extracted_result": ("ext.csv", buffer2.getvalue(), "text/csv")
        }
        
        response = client.post("/comparison/api/compare", files=files)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["success"] is True

    def test_workflow_with_mismatches(self, client):
        """Test workflow with files that have mismatches"""
        # Create test data with differences
        df1 = pd.DataFrame({
            'Item': ['A', 'B', 'C'],
            'Amount': [100, 200, 300]
        })
        df2 = pd.DataFrame({
            'Item': ['A', 'B', 'C'],
            'Amount': [100, 250, 300]  # Different value
        })
        
        buffer1 = io.BytesIO()
        buffer2 = io.BytesIO()
        df1.to_excel(buffer1, index=False, engine='openpyxl')
        df2.to_excel(buffer2, index=False, engine='openpyxl')
        buffer1.seek(0)
        buffer2.seek(0)
        
        # Upload and compare
        files = {
            "ground_truth": ("gt.xlsx", buffer1.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            "extracted_result": ("ext.xlsx", buffer2.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        }
        
        response = client.post("/comparison/api/compare", files=files)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["success"] is True
        assert data["result"]["mismatched_rows"] > 0
        
        # Check that mismatches have confidence values
        has_confidence = False
        for row in data["result"]["rows"]:
            for cell in row["cells"]:
                if not cell["match"]:
                    assert cell["confidence"] is not None
                    has_confidence = True
        
        assert has_confidence



