import boto3
import os
import json
import datetime

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

# Connect
def lambda_handler(event, context):
    print('DISCONNECTION')
    print('event:', event)
    
    # Fetch connection ID
    connection_id = event['requestContext']['connectionId']
    print('connectionId: ', connection_id)
    
    # Store connection ID in dynamo
    connection_table_name = os.environ['CONNECTION_TABLE_NAME']
    dynamodb = AwsHelper().getResource("dynamodb")
    connection_table = dynamodb.Table(connection_table_name)

    connection_table.delete_item(
        Key = { 'connectionId': connection_id }
    )

    return {    
        'statusCode': 200, 
        'body': 'Connection added' 
    }
