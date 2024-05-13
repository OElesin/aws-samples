#!/bin/bash
set -euo pipefail

STACK_NAME="demo-bedrock-kb-berlin-awsug"

aws cloudformation deploy --stack-name "$STACK_NAME" --template-file ./cloudformation/template.yaml --region us-east-1 --capabilities CAPABILITY_NAMED_IAM --no-fail-on-empty-changeset
aws cloudformation wait stack-create-complete --stack-name "$STACK_NAME" --region us-east-1


outputs=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --query 'Stacks[0].Outputs' --region us-east-1)
knowledge_base_id=$(echo "$outputs" | jq -r '.[] | select(.OutputKey == "KnowledgeBaseId") | .OutputValue')
data_source_id=$(echo "$outputs" | jq -r '.[] | select(.OutputKey == "BedrockDataSource") | .OutputValue')
echo "{\"knowledge_base_id\":\"$knowledge_base_id\",\"data_source_id\":\"$data_source_id\"}"


echo "Done Deploying Stack"

echo "Add repositories to S3 bucket"

python3 ./code/add_repositories_to_s3.py

echo "Index Bedrock Knowledgebase"

python3 ./code/run_bedrock_kb_index.py -k $knowledge_base_id -d $data_source_id

