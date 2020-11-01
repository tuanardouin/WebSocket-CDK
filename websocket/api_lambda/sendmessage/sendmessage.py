import boto3
import os
import json

from botocore.exceptions import ClientError
from botocore.client import Config
from boto3.dynamodb.conditions import Key

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
    print('SEND MESSAGE')
    print('event:', event)

    connection_table_name = os.environ['CONNECTION_TABLE_NAME']
    dynamodb = AwsHelper().getResource("dynamodb")
    connection_table = dynamodb.Table(connection_table_name)

    # Fetch message and connection ID
    body = json.loads(event['body'])
    print('body:', body)
    
    sender_connection_id = event['requestContext']['connectionId']

    connection_table_response_username = connection_table.query(
        KeyConditionExpression = Key('connectionId').eq(sender_connection_id)
    )
    sender_username = connection_table_response_username['Items'][0]['username']
    
    if sender_username == '':
        print('No username set - 403')
        return {    
            'statusCode': 403, 
            'body': 'Set up an username using : {"action":"setusername", "data":"YOUR USERNAME"} ' 
        }

    message = body['data']
    
    print('sender_connection_id: ', sender_connection_id)
    print('message: ', message)
    
    # Build API URL
    url = 'https://' + event['requestContext']['domainName'] + '/prod'
    api_client = boto3.client('apigatewaymanagementapi', endpoint_url=url)


    # Fetch all open connection id
    connection_table_response = connection_table.scan()

    for connection in connection_table_response['Items']:
        if connection['connectionId'] != sender_connection_id:
            print('sending to : >{}<'.format(connection['connectionId']))
            api_client.post_to_connection(
                Data = '[' + sender_username + '] ' + message,
                ConnectionId = connection['connectionId']
            )

    return {    
        'statusCode': 200, 
        'body': 'Message Sent' 
    }
