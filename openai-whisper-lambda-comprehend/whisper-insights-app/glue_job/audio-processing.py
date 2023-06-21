import sys
import subprocess
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import whisper
import boto3
import botocore

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'payload', 'bucket'])

s3 = boto3.resource('s3')

# initialize subprocess to install ffmpeg
subprocess.run(['sudo', 'yum', 'install', 'ffmpeg', '-y'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

object_key = args['payload']
s3_bucket = args['bucket']
local_file_path = f'/tmp/{object_key}'
print(object_key)


def download_file_from_s3():
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


model = whisper.load_model("base")
download_file_from_s3()

result = model.transcribe(local_file_path)

print("Result object type" , type(result))
print(result["text"])

job.commit()
