from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKey
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
import boto3
import json
import uvicorn
import auth

bedrock_rt_west_2 = boto3.client('bedrock-runtime', region_name='us-west-2')

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
]

prompt_template = "\nHuman:You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. Answer the question {question}.\n\nAssistant:"

modelId = 'anthropic.claude-v2'
accept = 'application/json'
contentType = 'application/json'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApiRequest(BaseModel):
    prompt: str


@app.post("/v1/completions", status_code=201)
async def get_bedrock_completion(api_request: ApiRequest, api_key: APIKey = Depends(auth.get_api_key)):
    """
    """
    try:
        prompt = api_request.prompt
        response = await bedrock_completion(prompt)
        return response
    except ValidationError as e:
        raise HTTPException(status_code=403, detail="Invalid bearer token.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")


async def bedrock_completion(request):
    """
    """
    prompt = prompt_template.format(question=request)
    payload = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 400,
        "temperature": 0.4,
        "top_p": 0.9,
    })
    response = bedrock_rt_west_2.invoke_model(
        body=payload, 
        modelId=modelId, 
        accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get('body').read())
    return {
        'model': modelId,
        "object": "text_completion",
        'choices': [
            {
                'text': response_body['completion']
            }
        ]
    }