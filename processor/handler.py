import json
import boto3
import os
import logging
from processor.utils.wine_processor import get_from_bucket, transform, save_to_bucket


logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def categorize_wines(event, context):
    try:
        logger.info("Received event: %s", json.dumps(event))

        if 'Records' in event and len(event['Records']) > 0:
            record = event['Records'][0]
            if record['eventSource'] == 'aws:s3':
                logger.info("Processing file: %s", record['s3']['object']['key'])
        
        # Retriving from s3 bucket
        red_df = get_from_bucket(s3, bucket_name, "red")
        white_df = get_from_bucket(s3, bucket_name, "white")


        if red_df.empty or white_df.empty:
            raise ValueError("One of the datasets is empty")
        
        # Transforming
        low_df, high_df = transform(s3, bucket_name, white_df, red_df)
        
        # Saving changes on s3 bucket
        save_to_bucket(s3, bucket_name, high_df, "high-quality-wines.json")
        save_to_bucket(s3, bucket_name, low_df, "low-quality-wines.json")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Processing complete',
                'stats': {
                    'high_quality': len(high_df),
                    'low_quality': len(low_df)
                }
            })
        }
    except Exception as e:
        logger.error("Fatal error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'event': event,
                'columns_red': list(red_df.columns) if 'red_df' in locals() else None,
                'columns_white': list(white_df.columns) if 'white_df' in locals() else None
            })
        }
