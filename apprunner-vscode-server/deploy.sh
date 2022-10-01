#!/usr/bin/env bash
set -eux

echo "Build docker image"
IMAGE_NAME="aws-apprunner-vscode-server"
ECR_PUBLIC_ALIAS="oelesin"

docker buildx build --platform=linux/amd64 -t ${IMAGE_NAME} .

echo "Authenticating to AWS ECR Public"
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws


PASSWD=$(cat ./vscode_passwd_file)

#echo "create ECR public repository"
#aws ecr-public create-repository \
#     --repository-name ${IMAGE_NAME} \
#     --catalog-data file://repositorycatalogdata.json \
#     --region us-east-1

docker tag ${IMAGE_NAME}:latest public.ecr.aws/${ECR_PUBLIC_ALIAS}/${IMAGE_NAME}

docker push public.ecr.aws/${ECR_PUBLIC_ALIAS}/${IMAGE_NAME}


echo "Deploying AWS CloudFormation Stack with App Runner Service"

aws cloudformation deploy --stack-name "aws-apprunner-vscode-server" \
  --template-file cloudformation/template.yaml \
  --parameter-overrides PublicECRIdentifier=public.ecr.aws/${ECR_PUBLIC_ALIAS}/${IMAGE_NAME}:latest VSCodePassword=${PASSWD} \
  --no-fail-on-empty-changeset
