

if [ "$1" ]; then
    if [ "$1" == "-d" ]; then
        echo "-d is provided. deleting the stack..."
        sam delete --profile ${deploy_profile} --region us-east-1 --stack-name dev-capstone-main --no-prompts
    fi
    
fi

echo "building the sam template"
sam build

echo "deploying the sam template"
sam deploy --profile ${deploy_profile} --stack-name dev-capstone-main --no-confirm-changeset