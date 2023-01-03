import json
import unittest
import sys
import os

try:
    from src.lambda_functions.users.common.jwt_token_service import TokenService, RequestModel
    from src.lambda_functions.users.common.user_service import UserService, UserModel
    print('loaded from path')
except:
    sys.path.insert(0, '../../../../src/lambda_functions/users/common')
    sys.path.insert(0, './src/lambda_functions/users/common')
    from jwt_token_service import TokenService, RequestModel
    from user_service import UserService, UserModel
    print('loaded from inserted path')

class MyTestCase(unittest.TestCase):
    

    def test_generate_bare_jwt(self):
        ts = TokenService()
        jwt = ts.encode_jwt_token()
        #print(f'jwt: {jwt}')
        self.assertIsNotNone(jwt)


    def test_decode_jwt(self):
        ts = TokenService()
        request = RequestModel()
        request.client_id = "123456789"
        request.email = "first.last@example.com"
        jwt = ts.encode_jwt_token(request=request)
        #print(f'jwt: {jwt}')
        self.assertIsNotNone(jwt)

        decoded = ts.decode_jwt_token(jwt)
        #print(f'decoded: {decoded}')

        self.assertIsNotNone(decoded)


    def test_token_jwt_with_scopes(self):
        user = self.helper_get_user()
        user.scopes = ['admin', 'user', 'tester']
        us = UserService(user)
        encoded = us.generate_token()
        #print (f'token encoded: {encoded}')
        self.assertIsNotNone(encoded)

        ts = TokenService()
        decoded = ts.decode_jwt_token(encoded)

        #print(f'token decoded: {decoded}')



    def test_token_jwt_with_out_scopes(self):
        user = self.helper_get_user()        
        us = UserService(user)
        encoded = us.generate_token()
        #print (f'token encoded: {encoded}')
        self.assertIsNotNone(encoded)

        ts = TokenService()
        decoded = ts.decode_jwt_token(encoded)

        #print(f'token decoded: {decoded}')

    def test_token_jwt_with_scopes_as_string(self):
        user = self.helper_get_user()
        user.scopes = "['admin', 'user', 'tester']"
        us = UserService(user)
        encoded = us.generate_token()
        #print (f'token encoded: {encoded}')
        self.assertIsNotNone(encoded)

        ts = TokenService()
        decoded = ts.decode_jwt_token(encoded)

        print(f'token decoded scopes as string: {decoded}')

    def test_decode_token_with_scopes_from_db(self):
        encoded = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWYiOiJhMDQzOTk3Zi0yNmM4LTQ0NTMtOTdkMS05YTRjNTYzZmEyM2YiLCJhdWQiOiJhcHBsaWNhdGlvbl9vbmUiLCJlbWFpbCI6ImpvaG4uc21pdGhAZXhhbXBsZS5jb20iLCJleHAiOjM2MCwic2NvcGVzIjoiWyAnIGEgZCBtIGkgbiAnICwgICAnIHUgcyBlIHIgJyAsICAgJyBzIHUgcCBlIHIgLSB1IHMgZSByICcgXSIsInVzZXIiOiJqb2huIHNtaXRoIn0.pWLq0GRPcXYS67_FPXrmV0_Whz9tNBIF44U2-cgTELM"
        ts = TokenService()
        decoded = ts.decode_jwt_token(encoded)

        #print(f'decoded db/jwt token: {decoded}')
        self.assertIsNotNone(decoded)

    def helper_get_user(self):
        user = UserModel()
        user.first_name = "john"
        user.last_name = "doe"
        user.email = "john.doe@example.com"
        user.application = "app_one"
        user.is_valid = True
        return user

    
if __name__ == '__main__':
    print(f'dir: {__file__}')
    unittest.main()