# 🍷 Wine Quality Categorizer

## API

**GET** `/display-wines/`

- **Parameter**: `quality` (required)  
  - Accepted values: `"low"` or `"high"`
- **Returns**: JSON list of wines matching the specified quality category
- **Local**:
  ```bash
  cd api
  uvicorn main:app --reload
  curl "http://localhost:8000/display-wines/?quality=high"
  ```

---

## Lambdas

### Watcher: Automatically triggered upon CSV file uploads to an S3 bucket.

**Functionality:**
- Invoke Process lambda

### Process: Main functionality 

**Functionality:**
- Retrieves `winequality-red.csv` and `winequality-white.csv` from S3
- Merges both datasets
- Categorizes wine quality:
  - `low`: quality ≤ 4  
  - `high`: quality ≥ 7
- Saves the categorized data as a JSON file back to S3

---

## Requirements
- requirements.txt