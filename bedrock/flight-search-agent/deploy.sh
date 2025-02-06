#!/usr/bin/env bash
set -eux

BASE_STACK_NAME="aws-bedrock-app-stack"
APP_STACK_NAME="bedrock-apprunner-api"
AWS_REGION="eu-west-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
IMAGE_NAME="bedrock-apprunner-api"

aws cloudformation deploy --template-file ./cloudformation/base.template.yaml --stack-name "${BASE_STACK_NAME}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --no-fail-on-empty-changeset

IMAGE_URI=$(aws cloudformation describe-stacks --stack-name ${BASE_STACK_NAME} --query 'Stacks[0].Outputs[?OutputKey == `BedrockApiAppEcrRepo`].OutputValue' --output text)

echo "Authenticating to AWS ECR"
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

docker buildx build --platform=linux/amd64 -t ${IMAGE_NAME} .

docker tag "${IMAGE_NAME}:latest" "${IMAGE_URI}"

docker push "${IMAGE_URI}"

echo "Deploying app stack"

aws cloudformation deploy --template-file ./cloudformation/apprunner.template.yaml --stack-name "${APP_STACK_NAME}" \
  --parameter-overrides ImageUri=${IMAGE_URI} \
  --capabilities CAPABILITY_NAMED_IAM \
  --no-fail-on-empty-changeset