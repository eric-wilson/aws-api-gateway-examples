

## ServerlessRestApi
Unresolved resource dependencies [ServerlessRestApi] in the Outputs block of the template

```yaml
UserLoginApi:
    Description: "API Gateway endpoint URL for Prod stage for User Login function"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/users/login/"
```

This error is caused since I'm using ServerlessHttpApi vs ServerlessRestApi