import pytest
import pandas as pd
import io
from pathlib import Path
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_excel_ground_truth():
    """Create a sample Excel file with both tabs for ground truth data"""
    gt_df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['Tokyo', 'Osaka', 'Kyoto'],
        'Amount': [1000.50, 2000.75, 3000.00]
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        gt_df.to_excel(writer, sheet_name='正解データ', index=False)
    buffer.seek(0)
    return buffer.getvalue()


@pytest.fixture
def sample_excel_extracted():
    """Create a sample Excel file with both tabs for extracted results (with some differences)"""
    gt_df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['Tokyo', 'Osaka', 'Kyoto'],
        'Amount': [1000.50, 2000.75, 3000.00]
    })
    ext_df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 36],  # Different: 35 -> 36
        'City': ['Tokyo', 'Osaka', 'Kyoto'],
        'Amount': [1000.50, 2000.75, 3000.00]
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        gt_df.to_excel(writer, sheet_name='正解データ', index=False)
        ext_df.to_excel(writer, sheet_name='Robota結果', index=False)
    buffer.seek(0)
    return buffer.getvalue()


@pytest.fixture
def sample_csv_ground_truth():
    """Create a sample CSV file for ground truth data"""
    df = pd.DataFrame({
        'Product': ['Item A', 'Item B', 'Item C'],
        'Price': [100, 200, 300],
        'Quantity': [10, 20, 30]
    })
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)
    return buffer.getvalue()


@pytest.fixture
def sample_csv_extracted():
    """Create a sample CSV file for extracted results"""
    df = pd.DataFrame({
        'Product': ['Item A', 'Item B', 'Item C'],
        'Price': [100, 200, 300],
        'Quantity': [10, 20, 30]
    })
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)
    return buffer.getvalue()


@pytest.fixture
def identical_files():
    """Create Excel file with identical tabs for perfect match testing"""
    df = pd.DataFrame({
        'Column1': ['Value1', 'Value2', 'Value3'],
        'Column2': [1, 2, 3],
        'Column3': [1.1, 2.2, 3.3]
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='正解データ', index=False)
        df.to_excel(writer, sheet_name='Robota結果', index=False)
    buffer.seek(0)
    return buffer.getvalue()



