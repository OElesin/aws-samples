from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Security, status
import boto3
from botocore.exceptions import ClientError
import json

# Create a Secrets Manager client
sm = boto3.client('secretsmanager')

# Define the name of the secret
secret_name = 'my-api-keys'


api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def load_api_keys():
    """
    Load API keys from AWS Secrets Manager
    """
    response = sm.get_secret_value(
        SecretId=secret_name
    )
    secret_value = json.loads(response['SecretString'])
    return secret_value['APIKeys']


api_keys = load_api_keys()


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )