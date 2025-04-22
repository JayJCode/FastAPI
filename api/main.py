from fastapi import FastAPI, Query, HTTPException
from botocore.exceptions import ClientError
from typing import Literal
import boto3
import json
import os


s3 = boto3.client('s3')
app = FastAPI()
bucket_name = os.environ['BUCKET_NAME']

@app.get("/display-wines/")
async def display_wines(quality: Literal["low", "high"] = Query(..., description="Wine quality (low/high)")):
    try:
        file_key = f"{quality}-quality-wines.json"
        
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        
        wines_data = json.loads(file_content)
        
        return {
            "quality": quality,
            "count": len(wines_data),
            "wines": wines_data
        }
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(status_code=404, detail=f"File {file_key} not found in bucket. Available files: {get_available_files()}")
        raise HTTPException(status_code=500, detail=str(e))

def get_available_files():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])]
    except:
        return "Could not list files"