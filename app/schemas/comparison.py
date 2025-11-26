from typing import List, Optional, Any
from pydantic import BaseModel


class CellComparison(BaseModel):
    """Represents the comparison result for a single cell"""
    value: Any
    ground_truth: Any
    extracted: Any
    match: bool
    confidence: Optional[float] = None  # Percentage (0-100)


class RowComparison(BaseModel):
    """Represents the comparison result for a single row"""
    row_index: int
    cells: List[CellComparison]


class ComparisonResult(BaseModel):
    """Complete comparison result"""
    headers: List[str]
    rows: List[RowComparison]
    total_rows: int
    matched_rows: int
    mismatched_rows: int
    total_cells: int
    matched_cells: int
    mismatched_cells: int
    accuracy: Optional[float] = None  # Percentage of cells that matched (0-100)
    average_mismatch_confidence: Optional[float] = None  # Average similarity of mismatched cells


class ComparisonResponse(BaseModel):
    """API response for comparison"""
    success: bool
    result: Optional[ComparisonResult] = None
    error: Optional[str] = None



