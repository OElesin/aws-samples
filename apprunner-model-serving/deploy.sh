#!/usr/bin/env bash
set -eux

echo "Build docker image"
IMAGE_NAME="aws-apprunner-deepset-haystack-serving"
ECR_PUBLIC_ALIAS="h5e5i4d2"

docker build -t ${IMAGE_NAME} .

echo "Authenticating to AWS ECR Public"
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

echo "create ECR public repository"
#aws ecr-public create-repository \
#     --repository-name ${IMAGE_NAME} \
#     --catalog-data file://repositorycatalogdata.json \
#     --region us-east-1

docker tag ${IMAGE_NAME}:latest public.ecr.aws/${ECR_PUBLIC_ALIAS}/${IMAGE_NAME}

docker push public.ecr.aws/${ECR_PUBLIC_ALIAS}/${IMAGE_NAME}


echo "Deploying AWS CloudFormation Stack with App Runner Service"

aws cloudformation deploy --stack-name "football-transfer-qna-service" \
  --template-file cloudformation/template.yaml \
  --parameter-overrides "PublicECRIdentifier=public.ecr.aws/${ECR_PUBLIC_ALIAS}/${IMAGE_NAME}:latest" \
  --no-fail-on-empty-changeset
