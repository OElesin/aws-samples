#!/usr/bin/env bash
set -eux

aws cloudformation deploy --template-file ./cloudformation/template.yaml --stack-name "aws-transcribe-langchain-chatbot" \
  --capabilities CAPABILITY_NAMED_IAM \
  --no-fail-on-empty-changeset
