import boto3
from botocore.exceptions import ClientError
import random
import string
import json

# Create a Secrets Manager client
sm = boto3.client('secretsmanager')

# Define the name of the secret
secret_name = 'my-api-keys'

my_api_keys = []
# Generate 100 random API keys
for i in range(50):
    api_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    
    # Create a dictionary containing the API key and its metadata
    my_api_keys.append(api_key)

secret_dict = {
    'APIKeys': my_api_keys
}
    
try:
    # Put the secret in Secrets Manager
    response = sm.create_secret(
        Name=secret_name,
        Description="API keys for Bedrock API access in Apple Shortcuts",
        SecretString=json.dumps(secret_dict)
    )
    
    print(response)
    print('Key saved to AWS Secrets Manager')
except ClientError as e:
    print("Failed to store API key:", e)