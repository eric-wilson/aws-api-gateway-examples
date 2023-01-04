

```bash
curl -d '{"username":"<user-name>", "password":"<password>"}' -H 'Content-Type: application/json' https://<api-gateway>/users/login



```

### Example


```bash

## post with body information
curl -d '{"username":"awslambda", "password":"awspassword"}' -H 'Content-Type: application/json' https://9upmghlrr7.execute-api.us-east-1.amazonaws.com/users/login


## post with headers
curl https://9upmghlrr7.execute-api.us-east-1.amazonaws.com/users/login \
    -H 'username: awslambda' \
     -H 'password: awspassword' \
     -H 'Content-Type: application/json' \
     -d ''


```


```bash
# get permissions
## bad (created with CF)
aws apigateway get-authorizer --rest-api-id jqvflakmug --authorizer-id 9tobd4 --profile geekcafe-dev

{
    "id": "9tobd4",
    "name": "HttpApiLambdaAuthorizer",
    "type": "REQUEST",
    "authType": "custom",
    "authorizerUri": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:484433161997:function:dev-capstone-HttpApiLambdaFunctionAuthorizer-nLIV9XPxGUyP/invocations",
    "authorizerCredentials": "arn:aws:iam::484433161997:role/dev-capstone-HttpApiLambdaFunctionAuthorizerRole-1N74KEA6CCI6O",
    "identitySource": "$request.header.Authorization"
}

## good (created with the console)
aws apigateway get-authorizer --rest-api-id jqvflakmug --authorizer-id vnomcr --profile geekcafe-dev

{
    "id": "vnomcr",
    "name": "manual",
    "type": "REQUEST",
    "authType": "custom",
    "authorizerUri": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:484433161997:function:dev-capstone-HttpApiLambdaFunctionAuthorizer-nLIV9XPxGUyP/invocations",
    "identitySource": "$request.header.Authorization",
    "authorizerResultTtlInSeconds": 5
}


# auto-bad
aws apigateway get-authorizer --rest-api-id ieiwqfmpr9 --authorizer-id yojhdh --profile geekcafe-dev


```

```

function_name="dev-capstone-HttpApiLambdaFunctionAuthorizer-nLIV9XPxGUyP"
statement_id="apigateway-invoke-permissions-abc123"
aws_region="us-east-1"
aws_account_id="484433161997"
api_gateway_id="jqvflakmug"
authorizer_id="authorizer-id"
profile_name="geekcafe-dev"


aws lambda add-permission \
    --function-name ${function_name} \
    --statement-id ${statement_id} \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:${aws_region}:${aws_account_id}:${api_gateway_id}/authorizers/${authorizer_id}" \
    --profile ${profile_name}


"Statement": "{\"Sid\":\"apigateway-invoke-permissions-abc123\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"apigateway.amazonaws.com\"},\"Action\":\"lambda:InvokeFunction\",\"Resource\":\"arn:aws:lambda:us-east-1:484433161997:function:dev-capstone-HttpApiLambdaFunctionAuthorizer-nLIV9XPxGUyP\",\"Condition\":{\"ArnLike\":{\"AWS:SourceArn\":\"arn:aws:execute-api:us-east-1:484433161997:jqvflakmug/authorizers/authorizer-id\"}}}

```

## Action Items
- [ ] API Gateway
    - [ ] Login
    - [ ] List Users (admin)
    - [ ] /users/{id}/get 


```json

{
  "Version": "2012-10-17",
  "Id": "default",
  "Statement": [
    {
      "Sid": "dev-capstone-main-HttpApiLambdaFunctionAuthorizerLoginUserPermission-109R3XKTFQ5JA",
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:us-east-1:484433161997:function:dev-capstone-main-HttpApiLambdaFunctionAuthorizer-Dui7D08Wp3GI",
      "Condition": {
        "ArnLike": {
          "AWS:SourceArn": "arn:aws:execute-api:us-east-1:484433161997:ieiwqfmpr9/*/POST/authorizer/"
        }
      }
    },
    {
      "Sid": "fb1513a7-a5ac-5f4a-826a-ae3b663de4d6",
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:us-east-1:484433161997:function:dev-capstone-main-HttpApiLambdaFunctionAuthorizer-Dui7D08Wp3GI",
      "Condition": {
        "ArnLike": {
          "AWS:SourceArn": "arn:aws:execute-api:us-east-1:484433161997:ieiwqfmpr9/authorizers/b68bbu"
        }
      }
    }
  ]
}

```

```json

{
      "Sid": "custom-to-make-it-work",
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:us-east-1:484433161997:function:dev-capstone-main-HttpApiLambdaFunctionAuthorizer-Dui7D08Wp3GI",
      "Condition": {
        "ArnLike": {
          "AWS:SourceArn": "arn:aws:execute-api:us-east-1:484433161997:ieiwqfmpr9/authorizers/yojhdh"
        }
      }
    }

```