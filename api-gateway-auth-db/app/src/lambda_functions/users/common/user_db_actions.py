import boto3
from boto3.dynamodb.conditions import Key

import logging
import datetime
import os
from hash_algo import generate_hashed_password, generate_user_id
from user_db_model import UserModel


location = "common/users"
log = logging.getLogger(f"{location}")

table_name = os.getenv("TABLE_NAME")
if table_name is None:
    table_name = "ApplicationTable"
dynamodb_client = boto3.client('dynamodb')
dynamodb_resource = boto3.resource('dynamodb')
table = dynamodb_resource.Table(table_name)

log.setLevel('INFO')


def get_application_users(application="application_one", min=True):

    filtering_exp = Key("sk").eq(f"app#{application}")

    index="gsi_sk_min"
    if not min:
        index ="gsi_sk"
    
    # query the sort key based on our gsi that is pointint to it
    response = table.query(
        IndexName=f"{index}",
        KeyConditionExpression=filtering_exp,        
    )
            

    return response


def get_user(username, application="application_one", include_attributes = False) -> UserModel: 
    
       
    if include_attributes: 
        response = dynamodb_client.get_item(
            TableName=table_name,
                Key={
                    'pk': {'S': f'user#{username}'},
                    'sk': {'S': f'app#{application}'}
                }
            )
    else:
        
        response = table.get_item(            
                Key={
                    'pk': f'user#{username}',
                    'sk': f'app#{application}'
                }
            )

    log.info(f'user response: {response}')

    return __load_user_object(response, f"username:{username} application:{application}")

def get_user_by_id(id, include_attributes = False) -> UserModel: 
    
    #user_id = generate_user_id(username, application)
    
    if include_attributes: 
        response = dynamodb_client.get_item(
            TableName=table_name,
                Key={
                    'gsi_id': {'S': f'user_id#{id}'}                    
                }
            )
    else:
        
        response = table.get_item(            
                Key={
                    'gsi_id': f'user_id#{id}',                    
                }
            )

    log.info(f'user response: {response}')
    return __load_user_object(response, f"id:{id}")
    


def __load_user_object(dynamodb_response, keys):


    try:
        if "Item" in dynamodb_response:
            item = dynamodb_response['Item']
            log.info(f'user item info: {item}')
            user = UserModel()
            user.first_name = item["first_name"]
            user.last_name = item["last_name"]
            user.email = str(item["pk"]).removeprefix("user#")
            user.id = str(item["gsi_id"]).removeprefix("user_id#")
            user.hashed_password = item["password"]
            user.scopes = item["scopes"]
            user.application = str(item["sk"]).removeprefix("app#")
            return user
        else:
            log.info(f'user not found for keys: {keys}')
            return None
    except Exception as e:
        log.error(f'error getting keys: {keys}. {str(e)}')
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
    if id is None:
        id = generate_user_id(username, application)
    dynamodb_client.put_item(
        TableName=f'{table_name}', 
        Item={
            'pk': {'S': f'user#{username}'},
            'sk':{'S':f'app#{application}'},            
            'gsi_id':{'S':f'user_id#{id}'},
            'password':{'S':f'{hashed_password}'},
            'first_name':{'S':f'{first_name}'},
            'last_name':{'S':f'{last_name}'},
            'updated_date_time_utc': {'S': f'{datetime.datetime.utcnow()}'},
            'scopes': {'S': f'{scopes}'}
            }
        )