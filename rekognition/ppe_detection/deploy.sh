#!/usr/bin/env bash

aws cloudformation deploy --template-file template.yaml --stack-name "PPEDemo" \
  --parameter-overrides AdminEmail=elesin.olalekan@gmail.com CreateCloudFrontDistribution=true ResourcePrefix=PPEDemo \
  --capabilities CAPABILITY_NAMED_IAM \
  --no-fail-on-empty-changeset