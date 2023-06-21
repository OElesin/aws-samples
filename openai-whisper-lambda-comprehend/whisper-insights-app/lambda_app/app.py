import whisper
import boto3
import botocore
import json


s3 = boto3.resource('s3')
local_file_path = f'/tmp/audio.mp3'
model = whisper.load_model("base")


def download_file_from_s3(s3_bucket, object_key):
    """
    Function to download audio file from S3
    :return:
    """
    try:
        s3.Bucket(s3_bucket).download_file(object_key, local_file_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


# Put model in evaluation mode for inferencing


def lambda_handler(event, context):
    s3_bucket = event['bucket']['name']
    object_key = event['object']['key']

    download_file_from_s3(s3_bucket, object_key)

    # result = model.transcribe(local_file_path)

    # print("Result object type" , type(result))
    print(model)

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "predicted_label": 'label',
            }
        )
    }
