# Data Structure Validation

## Overview

The application now performs **explicit validation** to ensure both tabs have identical data structures before comparison.

## Validation Checks

### 1. Column Count Validation ✅

**What it checks:**
- Number of columns in "正解データ" vs "Robota結果"

**Error example:**
```
Column count mismatch: '正解データ' has 3 columns, 
but 'Robota結果' has 2 columns. 
Both tabs must have the same number of columns.
```

### 2. Column Name Validation ✅

**What it checks:**
- Column names match exactly
- Column order is identical

**Error example:**
```
Column name mismatch between tabs:
  • Missing in 'Robota結果': City
  • Extra in 'Robota結果': Location
Both tabs must have identical column names in the same order.
```

## Implementation

Located in [`app/services/comparison.py`](file:///Users/lee.sangmin/Repo/Test%20module/app/services/comparison.py) (lines 32-60):

```python
# Get headers from both tabs
gt_headers = list(ground_truth_df.columns)
robota_headers = list(extracted_df.columns)

# Validate data structure: check if headers match
if gt_headers != robota_headers:
    # Check if it's just a column count mismatch
    if len(gt_headers) != len(robota_headers):
        raise ValueError(
            f"Column count mismatch: '正解データ' has {len(gt_headers)} columns, "
            f"but 'Robota結果' has {len(robota_headers)} columns. "
            f"Both tabs must have the same number of columns."
        )
    
    # Check for different column names
    missing_in_robota = set(gt_headers) - set(robota_headers)
    extra_in_robota = set(robota_headers) - set(gt_headers)
    
    error_msg = "Column name mismatch between tabs:\n"
    if missing_in_robota:
        error_msg += f"  • Missing in 'Robota結果': {', '.join(missing_in_robota)}\n"
    if extra_in_robota:
        error_msg += f"  • Extra in 'Robota結果': {', '.join(extra_in_robota)}\n"
    error_msg += "Both tabs must have identical column names in the same order."
    
    raise ValueError(error_msg)
```

## Test Results

### Test Case 1: Column Count Mismatch
**File:** `test_column_count_mismatch.xlsx`
- 正解データ: Name, Age, City (3 columns)
- Robota結果: Name, Age (2 columns)

**Result:** ✅ Validation caught the error
```json
{
  "detail": "Column count mismatch: '正解データ' has 3 columns, but 'Robota結果' has 2 columns. Both tabs must have the same number of columns."
}
```

### Test Case 2: Column Name Mismatch
**File:** `test_column_name_mismatch.xlsx`
- 正解データ: Name, Age, City
- Robota結果: Name, Age, Location

**Result:** ✅ Validation caught the error
```json
{
  "detail": "Column name mismatch between tabs:\n  • Missing in 'Robota結果': City\n  • Extra in 'Robota結果': Location\nBoth tabs must have identical column names in the same order."
}
```

### Test Case 3: Valid Structure
**File:** `test_comparison.xlsx`
- 正解データ: Name, Age, City
- Robota結果: Name, Age, City

**Result:** ✅ Comparison proceeds successfully

## What's NOT Validated

❌ **Row count** - Different number of rows is allowed
- The comparison uses `max_rows = max(len(ground_truth_df), len(extracted_df))`
- Missing rows are treated as empty/null values

❌ **Data types** - Column data types are not strictly validated
- Values are normalized during comparison
- Type mismatches may result in comparison failures but won't prevent the process

## Benefits

1. **Early error detection** - Users know immediately if their file structure is wrong
2. **Clear error messages** - Specific information about what's missing or different
3. **Prevents silent failures** - No more mysterious NaN values from reindexing
4. **Better UX** - Users can fix their Excel file before re-uploading
