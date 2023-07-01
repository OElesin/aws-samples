import json
import boto3
import os

runtime = boto3.client("sagemaker-runtime")

bart_summarizer_sm_ep = os.getenv('BART_SUMMARIZER_SM_EP_NAME')


def predict_summary(full_text):
    """
    Function to invoke sagemaker endpoint and generate summary
    using HuggingFace model
    :param full_text:
    :return:
    """
    content_type = 'application/json'
    payload = {
        'inputs': full_text
    }
    response = runtime.invoke_endpoint(
        EndpointName=bart_summarizer_sm_ep,
        ContentType=content_type,
        Body=json.dumps(payload)
    )
    raw_response_body = response['Body'].read().decode('utf-8')
    return json.loads(raw_response_body)[0]


def respond(data, status=501):
    return {
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,POST,PUT",
            "Access-Control-Allow-Origin": "*"
        },
        "statusCode": status,
        "body": json.dumps(data)
    }


def this_exist_not_null(param):
    """Check if parameter exists or not"""
    if (
            not param or
            len(param) < 1
    ):
        return False

    return True


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    request_method = event['httpMethod']
    request_body = event["body"]
    if request_method == 'OPTIONS':
        return respond("This is a pre-flight OPTIONS Request", 200)
    if request_method == 'POST':
        if not this_exist_not_null(request_body):
            return respond("Invalid parameters", 400)
        data = json.loads(request_body)
        full_text = data['FullText']
        summary_response = predict_summary(full_text)
        return respond(summary_response, 200)
    else:
        return respond('Not Allowed', 403)
