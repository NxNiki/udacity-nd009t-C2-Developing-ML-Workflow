# serializeImageData:

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event["s3_key"] ## TODO: fill in
    bucket = event["s3_bucket"]## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, "/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# makePrediction:

import json
import boto3
import base64

# Update your endpoint name
ENDPOINT = "image-classification-2025-04-03-05-45-18-812"
runtime = boto3.client('sagemaker-runtime')
def lambda_handler(event, context):
    # Decode image from base64
    image = base64.b64decode(event["body"]["image_data"])
    # Invoke SageMaker endpoint
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType='image/png',
        Body=image
    )

    # Get inference result
    result = response['Body'].read().decode('utf-8')
    
    # Update event and return
    event['body']["inferences"] = json.loads(result)
    
    return {
        'statusCode': 200,
        'body': event['body']
    }


# filterInference:

import json

THRESHOLD = .7

def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event["inferences"]
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = THRESHOLD ## TODO: fill in
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': event['body']
    }