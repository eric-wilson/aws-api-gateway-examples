#sam delete --profile geekcafe-dev --region us-east-1 --stack-name dev-capstone-main --no-prompts

sam build
sam deploy --profile geekcafe-dev --stack-name dev-capstone-main --no-confirm-changeset