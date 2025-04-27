# 🍷 Wine Quality Categorizer

## API

**GET** `/display-wines/`

- **Parameter**: `quality` (required)  
  - Accepted values: `"low"` or `"high"`

- **Returns**: JSON list of wines matching the specified quality category

- **CLI**:
  ```bash
  cd api
  uvicorn main:app --reload
  curl "http://localhost:8000/display-wines/?quality=high"
  ```

- **GUI**:
  http://127.0.0.1:8000/docs

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

---

## ESSENTIAL BEFORE ANY DEPLOYMENT!

### Docker image and ECR creation

  **In {ID/REGION} put your ECR id/region**
  ```aws ecr create-repository --repository-name wine-processor
  docker build -t wine-processor .
  docker tag wine-processor:latest {ID}.dkr.ecr.{REGION}.amazonaws.com/wine-processor:latest
  docker push {ID}.dkr.ecr.{REGION}.amazonaws.com/wine-processor:latest
  ```

  **Change ur ImageUri**
  (example)
  ```
  ECRUri:
    Type: String
    Default: 199215058137.dkr.ecr.eu-north-1.amazonaws.com/wine-processor:latest
    Description: ECR image URI for the wine processor
  ```
