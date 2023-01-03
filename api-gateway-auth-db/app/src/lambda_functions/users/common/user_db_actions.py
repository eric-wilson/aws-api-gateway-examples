import boto3
import logging
import datetime
from hash_algo import generate_hashed_password, generate_user_id
from user_db_model import UserModel


location = "common/users"
log = logging.getLogger(f"{location}")
table_name = "ApplicationTable"
dynamodb_client = boto3.client('dynamodb')
dynamodb_resource = boto3.resource('dynamodb')
table = dynamodb_resource.Table(table_name)

log.setLevel('INFO')


def get_user(username, application="application_one", include_attributes = False) -> UserModel: 
    
    user_id = generate_user_id(username, application)
    
    if include_attributes: 
        response = dynamodb_client.get_item(
            TableName=table_name,
                Key={
                    'pk': {'S': f'user-id#{user_id}'},
                    'sk': {'S': f'user#{username}'}
                }
            )
    else:
        
        response = table.get_item(            
                Key={
                    'pk': f'user-id#{user_id}',
                    'sk': f'user#{username}'
                }
            )

    log.info(f'user response: {response}')

    try:
        if "Item" in response:
            item = response['Item']
            log.info(f'user item info: {item}')
            user = UserModel()
            user.first_name = item["first_name"]
            user.last_name = item["last_name"]
            user.email = str(item["sk"]).removeprefix("user#")
            user.id = str(item["pk"]).removeprefix("user-id#")
            user.hashed_password = item["password"]
            user.scopes = item["scopes"]
            user.application = application
            return user
        else:
            log.info(f'user not found for {username} / {application}')
            return None
    except Exception as e:
        log.error(f'error getting user: {username} / {application}. {str(e)}')
        return None


def seed_users(event):
    log.info(f'todo: {location}')
    
    if "users" in event:
        users = event["users"]
        for user in users:
            scopes = ""
            id = None
            if "scopes" in user:
                scopes = user["scopes"]
            if "id" in user:
                id = user["id"]
            seed_user(
                id,
                user["username"],
                user["password"],
                user["application"],
                user["first_name"],
                user["last_name"],
                scopes
            )
    
    return False

def seed_user(id, username, password, application, first_name, last_name, scopes=''):

    hashed_password = generate_hashed_password(username, password, application)
    #if id is None:
    id = generate_user_id(username, application)
    dynamodb_client.put_item(
        TableName=f'{table_name}', 
        Item={
            'pk': {'S': f'user-id#{id}'},
            'sk':{'S':f'user#{username}'},            
            'app':{'S':f'{application}'},
            'password':{'S':f'{hashed_password}'},
            'first_name':{'S':f'{first_name}'},
            'last_name':{'S':f'{last_name}'},
            'updated_date_time_utc': {'S': f'{datetime.datetime.utcnow()}'},
            'scopes': {'S': f'{scopes}'}
            }
        )