# 🍷 Wine Quality Categorizer

## API Endpoint

**GET** `/display-wines/`

- **Parameter**: `quality` (required)  
  - Accepted values: `"low"` or `"high"`
- **Returns**: JSON list of wines matching the specified quality category
- **Example**:
  ```bash
  curl "http://localhost:8000/display-wines/?quality=high"
  ```

---

## Lambda Function

**Trigger**: Automatically triggered upon CSV file uploads to an S3 bucket.

### Functionality:
- Retrieves `winequality-red.csv` and `winequality-white.csv` from S3
- Merges both datasets
- Categorizes wine quality:
  - `low`: quality ≤ 4  
  - `high`: quality ≥ 7
- Saves the categorized data as a JSON file back to S3

### Required Permissions:
- S3 (Read/Write)
- CloudWatch Logs

---

## Requirements

- Python 3.12  
- AWS CLI (for deployment)  
- Python Libraries:  
  - `pandas`  
  - `boto3`  
  - `fastapi`
