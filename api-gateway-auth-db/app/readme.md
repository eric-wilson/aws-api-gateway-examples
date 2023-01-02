

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

## Action Items
- [ ] API Gateway
    - [ ] Login
    - [ ] List Users (admin)
    - [ ] /users/{id}/get 