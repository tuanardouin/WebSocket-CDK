import boto3
import os
import json

from botocore.exceptions import ClientError
from botocore.client import Config

class AwsHelper:
    def getResource(self, name, awsRegion=None):
        config = Config(
            retries = dict(
                max_attempts = 30
            )
        )

        if(awsRegion):
            return boto3.resource(name, region_name=awsRegion, config=config)
        else:
            return boto3.resource(name, config=config)


# Send message
def lambda_handler(event, context):
    print('SET USERNAME')
    print('event:', event)

    # Fetch message and connection ID
    body = json.loads(event['body'])
    print('body:', body)
    
    sender_connection_id = event['requestContext']['connectionId']
    username = body['data']
    
    print('sender_connection_id: ', sender_connection_id)
    print('username: ', username)

    # Fetch all open connection id
    connection_table_name = os.environ['CONNECTION_TABLE_NAME']
    dynamodb = AwsHelper().getResource("dynamodb")
    connection_table = dynamodb.Table(connection_table_name)

    connection_table.update_item(
        Key = { 'connectionId': sender_connection_id },
        UpdateExpression = 'SET username = :usernameValue',
        ConditionExpression = 'attribute_exists(connectionId)',
        ExpressionAttributeValues = {
            ':usernameValue': username
        }
    )

    return {    
        'statusCode': 200, 
        'body': 'Usernmame set' 
    }
