#!/usr/bin/env bash
set -eux

BASE_STACK_NAME="aws-transcribe-langchain-chatbot"

aws cloudformation deploy --template-file ./cloudformation/template.yaml --stack-name "${BASE_STACK_NAME}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --no-fail-on-empty-changeset
