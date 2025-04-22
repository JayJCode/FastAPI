import logging
import pandas as pd
from io import StringIO


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_from_bucket(s3, bucket_name, dvalue):
    try:
        file_key = f"winequality-{dvalue}.csv"
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        return pd.read_csv(StringIO(file_content), sep=";")

    except Exception as e:
        logger.error(f"Error loading {dvalue} wine: {str(e)}")
        raise

def transform(s3, bucket_name, white_wine, red_wine):
    try:
        # Validation
        for df, name in [(white_wine, 'white'), (red_wine, 'red')]:
            if 'quality' not in df.columns:
                raise ValueError(f"Column 'quality' missing in {name} wine data")
        
        # Adding wine type
        white_wine["wine_type"] = "white"
        red_wine["wine_type"] = "red"

        # Merging
        wines = pd.concat([white_wine, red_wine])

        # Filtering
        high_quality = wines[wines["quality"] >= 7].copy()
        low_quality = wines[wines["quality"] <= 4].copy()
        
        return low_quality, high_quality
        
    except Exception as e:
        logger.error(f"Transform error: {str(e)}")
        raise

def save_to_bucket(s3, bucket_name, df, filename):
    json_data = df.to_json(orient='records')
    
    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=json_data,
        ContentType='application/json'
    )