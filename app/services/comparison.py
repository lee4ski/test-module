import io
import logging
import os
import pandas as pd
from typing import Any, Optional
from difflib import SequenceMatcher

from app.schemas.comparison import (
    CellComparison,
    RowComparison,
    ComparisonResult,
)

# Optional OpenAI import
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

logger = logging.getLogger(__name__)


class ComparisonService:
    """Service for comparing ground truth data with extracted results"""

    def __init__(self):
        """Initialize the comparison service with optional LLM client"""
        self.llm_client = None
        # Try to initialize OpenAI client if API key is available
        if not OPENAI_AVAILABLE:
            logger.info("OpenAI package not installed. Will use rule-based column matching.")
            return
            
        openai_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        if openai_api_key:
            try:
                # Check if it's Azure OpenAI
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
                if azure_endpoint:
                    self.llm_client = OpenAI(
                        api_key=openai_api_key,
                        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
                        base_url=f"{azure_endpoint}/openai/deployments/{os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')}",
                    )
                else:
                    # Regular OpenAI - simple initialization
                    self.llm_client = OpenAI(api_key=openai_api_key)
                logger.info("LLM client initialized for column matching")
            except Exception as e:
                logger.warning(f"Failed to initialize LLM client: {e}. Will use rule-based matching.")
                self.llm_client = None
        else:
            logger.info("No OpenAI API key found. Will use rule-based column matching.")

    def compare_files(
        self, excel_file: bytes
    ) -> ComparisonResult:
        """
        Compare two tabs within a single Excel file and generate comparison results with confidence levels.

        Args:
            excel_file: Bytes content of the Excel file containing both tabs

        Returns:
            ComparisonResult with detailed comparison data
        """
        # Parse Excel file and read specific tabs
        ground_truth_df = self._parse_excel_sheet(excel_file, "正解データ")
        extracted_df = self._parse_excel_sheet(excel_file, "Robota結果")

        # Get headers from both tabs
        gt_headers = [str(h).strip() for h in ground_truth_df.columns]
        robota_headers = [str(h).strip() for h in extracted_df.columns]

        # Match columns by name (order-independent, with LLM or fuzzy matching)
        if self.llm_client:
            try:
                column_mapping = self._match_columns_with_llm(gt_headers, robota_headers)
                logger.info(f"LLM matched {len(column_mapping)} columns")
            except Exception as e:
                logger.warning(f"LLM column matching failed: {e}. Falling back to rule-based matching.")
                column_mapping = self._match_columns(gt_headers, robota_headers)
        else:
            column_mapping = self._match_columns(gt_headers, robota_headers)
        
        # Validate that we can match all columns
        unmatched_gt = [col for col in gt_headers if col not in column_mapping]
        if unmatched_gt:
            # Try fallback: match by position if column counts match
            if len(gt_headers) == len(robota_headers):
                # Use position-based matching as fallback for unmatched columns
                used_robota = set(column_mapping.values())
                available_robota = [col for col in robota_headers if col not in used_robota]
                
                # Try to match remaining columns by position
                for i, gt_col in enumerate(gt_headers):
                    if gt_col not in column_mapping:
                        # Try to find a match in available columns by position
                        if i < len(available_robota):
                            column_mapping[gt_col] = available_robota[i]
                            used_robota.add(available_robota[i])
                            available_robota = [col for col in robota_headers if col not in used_robota]
                
                # Re-check if all are now matched
                unmatched_gt = [col for col in gt_headers if col not in column_mapping]
            
            # If still unmatched, try fuzzy matching on remaining columns
            if unmatched_gt:
                used_robota = set(column_mapping.values())
                available_robota = [col for col in robota_headers if col not in used_robota]
                
                for gt_col in unmatched_gt[:]:  # Copy list to modify during iteration
                    best_match = None
                    best_similarity = 0.0
                    gt_normalized = str(gt_col).strip().lower()
                    
                    for robota_col in available_robota:
                        robota_normalized = str(robota_col).strip().lower()
                        similarity = SequenceMatcher(None, gt_normalized, robota_normalized).ratio()
                        if similarity > best_similarity and similarity >= 0.5:  # Lower threshold for final attempt
                            best_similarity = similarity
                            best_match = robota_col
                    
                    if best_match:
                        column_mapping[gt_col] = best_match
                        used_robota.add(best_match)
                        available_robota = [col for col in robota_headers if col not in used_robota]
                        unmatched_gt.remove(gt_col)
                        logger.info(f"Fuzzy matched '{gt_col}' -> '{best_match}' (similarity: {best_similarity:.2%})")
            
            # Final check - if still unmatched, allow comparison to proceed with warning
            if unmatched_gt:
                used_robota = set(column_mapping.values())
                available_cols = [col for col in robota_headers if col not in used_robota]
                
                # Log warning but allow comparison to proceed
                logger.warning(
                    f"Some columns couldn't be matched: {unmatched_gt}. "
                    f"These columns will be compared as None/empty in the extracted data."
                )
                
                # For unmatched columns, we'll compare against None/empty values
                # This allows the comparison to proceed rather than failing
        
        # Use ground truth headers as the reference order
        headers = gt_headers

        # Compare row by row
        rows = []
        matched_row_count = 0
        mismatched_row_count = 0
        matched_cell_count = 0
        mismatched_cell_count = 0
        total_confidence = 0.0
        confidence_count = 0

        max_rows = max(len(ground_truth_df), len(extracted_df))

        for i in range(max_rows):
            row_cells = []
            row_matches = True

            for col in headers:
                # Get ground truth value
                gt_value = (
                    ground_truth_df.iloc[i][col]
                    if i < len(ground_truth_df)
                    else None
                )
                # Get extracted value using column mapping
                mapped_col = column_mapping.get(col)
                if mapped_col and mapped_col in extracted_df.columns:
                    ext_value = (
                        extracted_df.iloc[i][mapped_col] if i < len(extracted_df) else None
                    )
                else:
                    # Column not matched - compare against None/empty
                    ext_value = None
                    if col not in column_mapping:
                        logger.debug(f"Column '{col}' not matched, comparing against None")

                # Normalize values for comparison
                gt_normalized = self._normalize_value(gt_value)
                ext_normalized = self._normalize_value(ext_value)

                # Check if values match
                matches = gt_normalized == ext_normalized

                # Count cell matches/mismatches
                if matches:
                    matched_cell_count += 1
                else:
                    mismatched_cell_count += 1
                    row_matches = False

                # Calculate confidence if mismatch
                confidence = None
                if not matches:
                    confidence = self._calculate_confidence(
                        gt_normalized, ext_normalized
                    )
                    total_confidence += confidence
                    confidence_count += 1

                # Convert numpy types to native Python types for JSON serialization
                gt_value_clean = self._convert_to_native(gt_value)
                ext_value_clean = self._convert_to_native(ext_value)
                
                cell_comparison = CellComparison(
                    value=gt_value_clean,
                    ground_truth=gt_value_clean,
                    extracted=ext_value_clean,
                    match=matches,
                    confidence=confidence,
                )
                row_cells.append(cell_comparison)

            if row_matches:
                matched_row_count += 1
            else:
                mismatched_row_count += 1

            rows.append(RowComparison(row_index=i, cells=row_cells))

        # Calculate total cells
        total_cells = matched_cell_count + mismatched_cell_count

        # Calculate accuracy: percentage of cells that matched
        accuracy = (
            (matched_cell_count / total_cells * 100) if total_cells > 0 else 100.0
        )

        # Calculate average confidence of mismatched cells (for reference)
        average_mismatch_confidence = (
            (total_confidence / confidence_count) if confidence_count > 0 else None
        )

        return ComparisonResult(
            headers=[str(h) for h in headers],  # Ensure headers are strings
            rows=rows,
            total_rows=int(max_rows),
            matched_rows=int(matched_row_count),
            mismatched_rows=int(mismatched_row_count),
            total_cells=int(total_cells),
            matched_cells=int(matched_cell_count),
            mismatched_cells=int(mismatched_cell_count),
            accuracy=round(accuracy, 2),
            average_mismatch_confidence=round(average_mismatch_confidence, 2) if average_mismatch_confidence is not None else None,
        )

    def _parse_file(self, file_content: bytes) -> pd.DataFrame:
        """Parse Excel or CSV file from bytes"""
        file_obj = io.BytesIO(file_content)

        # Try Excel first
        try:
            # Try reading as Excel (xlsx, xls)
            df = pd.read_excel(file_obj, engine="openpyxl")
            return df
        except Exception:
            pass

        # Try CSV
        try:
            file_obj.seek(0)
            df = pd.read_csv(file_obj, encoding="utf-8")
            return df
        except Exception:
            pass

        # Try CSV with different encoding
        try:
            file_obj.seek(0)
            df = pd.read_csv(file_obj, encoding="shift_jis")
            return df
        except Exception as e:
            pass

        # If all attempts failed, raise an error
        raise ValueError("Unable to parse file. Supported formats: Excel (.xlsx, .xls) and CSV. Please ensure the file is a valid Excel or CSV file.")

    def _parse_excel_sheet(self, file_content: bytes, sheet_name: str) -> pd.DataFrame:
        """Parse a specific sheet from an Excel file"""
        file_obj = io.BytesIO(file_content)
        
        try:
            # Read specific sheet from Excel file
            df = pd.read_excel(file_obj, sheet_name=sheet_name, engine="openpyxl")
            return df
        except ValueError as e:
            # Sheet not found
            raise ValueError(f"Sheet '{sheet_name}' not found in Excel file. Please ensure the file contains both '正解データ' and 'Robota結果' tabs.")
        except Exception as e:
            raise ValueError(f"Unable to read Excel file. Error: {str(e)}")


    def _normalize_value(self, value: Any) -> str:
        """Normalize value for comparison"""
        if value is None or pd.isna(value):
            return ""
        if isinstance(value, (int, float)):
            # Normalize numbers - remove trailing zeros
            if isinstance(value, float) and value.is_integer():
                return str(int(value))
            return str(value)
        return str(value).strip()

    def _calculate_confidence(
        self, ground_truth: str, extracted: str
    ) -> float:
        """
        Calculate confidence level (0-100) based on similarity between two strings.
        Uses sequence matching to determine similarity percentage.
        """
        if not ground_truth and not extracted:
            return 100.0
        if not ground_truth or not extracted:
            return 0.0

        # Use SequenceMatcher for similarity
        similarity = SequenceMatcher(None, ground_truth, extracted).ratio()
        return round(similarity * 100, 2)

    def _match_columns_with_llm(self, gt_headers: list, robota_headers: list) -> dict:
        """
        Use LLM to semantically match columns between ground truth and extracted data.
        This can handle:
        - Different languages (e.g., "Name" vs "名前")
        - Semantic similarity (e.g., "Amount" vs "金額")
        - Abbreviations (e.g., "First Name" vs "FName")
        - Different naming conventions
        
        Returns:
            dict mapping ground truth column names to extracted column names
        """
        if not self.llm_client:
            raise ValueError("LLM client not initialized")
        
        # Create a prompt for the LLM
        prompt = f"""You are a data matching expert. Match columns from two datasets based on their semantic meaning, not just exact name matching.

Ground Truth Columns (正解データ): {gt_headers}
Extracted Columns (Robota結果): {robota_headers}

Task: Create a mapping from Ground Truth column names to Extracted column names.
- Match columns that represent the same data, even if names are different
- Handle different languages (Japanese, English, etc.)
- Handle abbreviations and different naming conventions
- Handle columns with additional text in parentheses or different formatting (e.g., "source_file ファイル名" matches "ファイル名(正解データ)")
- Extract the core meaning: ignore prefixes like "source_file", suffixes in parentheses, extra spaces
- Each Ground Truth column should map to exactly one Extracted column
- Each Extracted column can only be used once
- If a Ground Truth column has no matching Extracted column, omit it from the mapping (this is OK - some columns may be missing)
- Focus on matching the Japanese text parts when column names have both English and Japanese

Return ONLY a JSON object in this format:
{{"column_mapping": {{"GroundTruthColumn1": "ExtractedColumn1", "GroundTruthColumn2": "ExtractedColumn2", ...}}, "unmatched_gt": ["ColumnName1", ...], "unmatched_robota": ["ColumnName1", ...]}}

The "unmatched_gt" array should list Ground Truth columns that couldn't be matched.
The "unmatched_robota" array should list Extracted columns that weren't used in the mapping.

Example:
If Ground Truth has ["source_file ファイル名", "Name", "Age"] and Extracted has ["ファイル名(正解データ)", "名前", "年齢"], return:
{{"column_mapping": {{"source_file ファイル名": "ファイル名(正解データ)", "Name": "名前", "Age": "年齢"}}, "unmatched_gt": [], "unmatched_robota": []}}

Now provide the mapping for the columns above:"""

        try:
            # Check if it's Azure OpenAI
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            if azure_endpoint:
                model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
            else:
                model = "gpt-4o"
            
            response = self.llm_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that returns only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"} if not azure_endpoint else None,
            )
            
            import json
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            column_mapping = result.get("column_mapping", {})
            unmatched_gt = result.get("unmatched_gt", [])
            
            # Validate the mapping
            if not isinstance(column_mapping, dict):
                raise ValueError("LLM returned invalid mapping format")
            
            # Ensure all values are valid column names
            valid_mapping = {}
            for gt_col, robota_col in column_mapping.items():
                if gt_col in gt_headers and robota_col in robota_headers:
                    valid_mapping[gt_col] = robota_col
                else:
                    logger.warning(f"LLM suggested invalid mapping: {gt_col} -> {robota_col}")
            
            # Log unmatched columns for debugging
            if unmatched_gt:
                logger.info(f"LLM identified unmatched Ground Truth columns: {unmatched_gt}")
            
            return valid_mapping
            
        except Exception as e:
            logger.error(f"Error in LLM column matching: {e}")
            raise

    def _match_columns(self, gt_headers: list, robota_headers: list) -> dict:
        """
        Match columns between ground truth and extracted data.
        Uses exact matching first, then fuzzy matching for similar names.
        
        Returns:
            dict mapping ground truth column names to extracted column names
        """
        column_mapping = {}
        used_robota_cols = set()
        
        # Normalize all headers first (handle None, NaN, etc.)
        gt_headers_clean = [str(h).strip() if h is not None and str(h).strip() != 'nan' else '' for h in gt_headers]
        robota_headers_clean = [str(h).strip() if h is not None and str(h).strip() != 'nan' else '' for h in robota_headers]
        
        # First pass: exact matches (case-insensitive, whitespace-insensitive)
        for i, gt_col in enumerate(gt_headers):
            gt_col_normalized = gt_headers_clean[i].lower()
            if not gt_col_normalized:  # Skip empty column names
                continue
                
            for j, robota_col in enumerate(robota_headers):
                if j in used_robota_cols:
                    continue
                    
                robota_col_normalized = robota_headers_clean[j].lower()
                if not robota_col_normalized:  # Skip empty column names
                    continue
                    
                if gt_col_normalized == robota_col_normalized:
                    column_mapping[gt_col] = robota_col
                    used_robota_cols.add(j)
                    break
        
        # Second pass: fuzzy matching for remaining columns (lower threshold for better matching)
        for i, gt_col in enumerate(gt_headers):
            if gt_col in column_mapping:
                continue
                
            gt_col_normalized = gt_headers_clean[i].lower()
            if not gt_col_normalized:
                continue
                
            best_match = None
            best_match_idx = None
            best_similarity = 0.0
            
            for j, robota_col in enumerate(robota_headers):
                if j in used_robota_cols:
                    continue
                    
                robota_col_normalized = robota_headers_clean[j].lower()
                if not robota_col_normalized:
                    continue
                    
                # Calculate similarity
                similarity = SequenceMatcher(None, gt_col_normalized, robota_col_normalized).ratio()
                if similarity > best_similarity and similarity >= 0.6:  # Lowered threshold to 60% for better matching
                    best_similarity = similarity
                    best_match = robota_col
                    best_match_idx = j
            
            if best_match:
                column_mapping[gt_col] = best_match
                used_robota_cols.add(best_match_idx)
        
        return column_mapping

    def _convert_to_native(self, value: Any) -> Any:
        """Convert numpy/pandas types to native Python types for JSON serialization"""
        import numpy as np
        
        if value is None or pd.isna(value):
            return None
        if isinstance(value, (np.integer, np.int64, np.int32)):
            return int(value)
        if isinstance(value, (np.floating, np.float64, np.float32)):
            return float(value)
        if isinstance(value, np.bool_):
            return bool(value)
        if isinstance(value, (int, float, str, bool)):
            return value
        # For any other type, convert to string
        return str(value)

