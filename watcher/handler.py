import boto3
import os
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    try:
        logger.info("New file uploaded: %s", event)
        
        lambda_client = boto3.client('lambda')
        processor_function = os.environ['PROCESSOR_FUNCTION']
        
        response = lambda_client.invoke(
            FunctionName=processor_function,
            InvocationType='Event',
            Payload=json.dumps(event)
        )
        
        logger.info("Processor invoked: %s", response)
        
    except Exception as e:
        logger.error("Watcher error: %s", str(e))
        raise