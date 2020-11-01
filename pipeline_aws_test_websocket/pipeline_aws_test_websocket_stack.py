import random

from aws_cdk import core


from aws_cdk import (
    aws_cloudformation as cfn,
    aws_logs as cwlogs,
    aws_lambda,
    aws_lambda_python as py_lambda,
    aws_apigatewayv2 as apiv2,
    aws_iam as iam,
    aws_route53 as r53,
    aws_certificatemanager as acm,
    aws_dynamodb as dynamodb,
    core,
)


class WebsocketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        brand = 'a'
        stage = 'dev'
        tablename = 'webchat'

        connectionstable = dynamodb.Table(self, 'connectionsTable',
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY,
            table_name = tablename,
            partition_key=dynamodb.Attribute(name="connectionId", type=dynamodb.AttributeType.STRING),
        )

        websocketgw = apiv2.CfnApi(self, 'websocket',
            name =  'SimpleChatWebSocket',
            protocol_type = 'WEBSOCKET',
            route_selection_expression = '$request.body.action'
        )

        # connect function
        connect_function =  py_lambda.PythonFunction(self, "connect_function",
            entry= 'websocket/api_lambda/connect',                            #folder
            index = 'connect.py',                           #file
            handler = 'lambda_handler',                 #function
            description = 'connect',
            environment = {
                'brand':brand,
                'stage':stage,
                'CONNECTION_TABLE_NAME': tablename},
            timeout = core.Duration.seconds(60)
        )
        connectionstable.grant_read_write_data(connect_function)

        connect_function_policy = iam.Policy(self, 'connect_policy',
            statements= [
                iam.PolicyStatement(
                    actions = ['dynamodb:*'],
                    resources = [connectionstable.table_arn]  
                )
            ],
            roles= [connect_function.role]
        )

        connect_function_permission = aws_lambda.CfnPermission(self, 'connectFunctionPermission',
            action = 'lambda:InvokeFunction',
            function_name = connect_function.function_name,
            principal = 'apigateway.amazonaws.com'
        )
        connect_function_permission.add_depends_on(websocketgw)


        # # disconnect function
        disconnect_function =  py_lambda.PythonFunction(self, "disconnect_function",
            entry= 'websocket/api_lambda/disconnect',                            #folder
            index = 'disconnect.py',                           #file
            handler = 'lambda_handler',                 #function
            description = 'disconnect',
            environment = {
                'brand':brand,
                'stage':stage,
                'CONNECTION_TABLE_NAME': tablename},
            timeout = core.Duration.seconds(60)
        )

        disconnect_function_policy = iam.Policy(self, 'disconnect_policy',
            statements= [
                iam.PolicyStatement(
                    actions = ['dynamodb:*'],
                    resources = [connectionstable.table_arn]  
                )
            ],
            roles= [disconnect_function.role]
        )

        disconnect_function_permission = aws_lambda.CfnPermission(self, 'disconnectFunctionPermission',
            action = 'lambda:InvokeFunction',
            function_name = disconnect_function.function_name,
            principal = 'apigateway.amazonaws.com'
        )
        connectionstable.grant_read_write_data(disconnect_function)
        disconnect_function_permission.add_depends_on(websocketgw)

        #send message function.
        sendmessage_function =  py_lambda.PythonFunction(self, "sendmessage_function",
            entry= 'websocket/api_lambda/sendmessage',                            #folder
            index = 'sendmessage.py',                                             #file
            handler = 'lambda_handler',                                           #function
            description = 'sendmessage',
            environment = {
                'brand':brand,
                'stage':stage,
                'CONNECTION_TABLE_NAME': tablename
            },
            timeout = core.Duration.seconds(60)
        )
        connectionstable.grant_read_write_data(connect_function)

        sendmessage_function_policy = iam.Policy(self, 'sendmessage_policy',
            statements= [
                iam.PolicyStatement(
                    actions = ['dynamodb:*'],
                    resources = [connectionstable.table_arn]  
                ),
                iam.PolicyStatement(
                    actions = ['execute-api:ManageConnections'],
                    resources= [
                        f'arn:aws:execute-api:aws:{self.region}:{self.account}:{websocketgw.ref}/*',
                        f'arn:aws:execute-api:{self.region}:{self.account}:{websocketgw.ref}/prod/POST/@connections/*'
                    ],
                ),
            ],
            roles= [sendmessage_function.role]        
        )
        sendmessage_function_permission = aws_lambda.CfnPermission(self, 'sendmessageFunctionPermission',
            action = 'lambda:InvokeFunction',
            function_name = sendmessage_function.function_name,
            principal = 'apigateway.amazonaws.com'
        )
        sendmessage_function_permission.add_depends_on(websocketgw)


        #set username function
        setusername_function =  py_lambda.PythonFunction(self, "setusername_function",
            entry= 'websocket/api_lambda/setusername',                            #folder
            index = 'setusername.py',                                             #file
            handler = 'lambda_handler',                                           #function
            description = 'setusername',
            environment = {
                'brand':brand,
                'stage':stage,
                'CONNECTION_TABLE_NAME': tablename
            },
            timeout = core.Duration.seconds(60)
        )
        connectionstable.grant_read_write_data(connect_function)

        setusername_function_policy = iam.Policy(self, 'setusername_policy',
            statements= [
                iam.PolicyStatement(
                    actions = ['dynamodb:*'],
                    resources = [connectionstable.table_arn]  
                ),
                iam.PolicyStatement(
                    actions = ['execute-api:ManageConnections'],
                    resources= [
                        f'arn:aws:execute-api:aws:{self.region}:{self.account}:{websocketgw.ref}/*',
                        f'arn:aws:execute-api:{self.region}:{self.account}:{websocketgw.ref}/prod/POST/@connections/*'
                    ],
                ),
            ],
            roles= [setusername_function.role]        
        )
        setusername_function_permission = aws_lambda.CfnPermission(self, 'setusernameFunctionPermission',
            action = 'lambda:InvokeFunction',
            function_name = setusername_function.function_name,
            principal = 'apigateway.amazonaws.com'
        )
        setusername_function_permission.add_depends_on(websocketgw)


        # Connect route
        connect_integration = apiv2.CfnIntegration(self, 'ConnectIntegration',
            api_id = websocketgw.ref,
            description= 'Connect Integration',
            integration_type = 'AWS_PROXY',
            integration_uri = f'arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{connect_function.function_arn}/invocations'
        )  
        
        connect_route = apiv2.CfnRoute(self, 'connectRoute',
            api_id = websocketgw.ref,
            route_key = '$connect',
            authorization_type = 'NONE',
            operation_name = 'ConnectRoute',
            target = 'integrations/' + connect_integration.ref 
        )

        # #Disconnect route
        disconnect_integration = apiv2.CfnIntegration(self, 'disConnectIntegration',
            api_id = websocketgw.ref,
            description= 'disConnect Integration',
            integration_type = 'AWS_PROXY',
            integration_uri = f'arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{disconnect_function.function_arn}/invocations'

        ) 
        disconnect_route = apiv2.CfnRoute(self, 'disconnectRoute',
            api_id = websocketgw.ref,
            route_key = '$disconnect',
            authorization_type = 'NONE',
            operation_name = 'DisconnectRoute',
            target = 'integrations/' + disconnect_integration.ref 
        )

        #Send Route
        sendmessage_integration = apiv2.CfnIntegration(self, 'sendMessageIntegration',
            api_id = websocketgw.ref,
            description= 'sendmessage Integration',
            integration_type = 'AWS_PROXY',
            integration_uri = f'arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{sendmessage_function.function_arn}/invocations'
        ) 
        sendmessage_route = apiv2.CfnRoute(self, 'sendRoute',
            api_id = websocketgw.ref,
            route_key = 'sendmessage',
            authorization_type = 'NONE',
            operation_name = 'SendRoute',
            target = 'integrations/' + sendmessage_integration.ref 
        )

        #Set username Route
        setusername_integration = apiv2.CfnIntegration(self, 'setUsernameIntegration',
            api_id = websocketgw.ref,
            description= 'setusername Integration',
            integration_type = 'AWS_PROXY',
            integration_uri = f'arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{setusername_function.function_arn}/invocations'
        ) 
        setusername_route = apiv2.CfnRoute(self, 'setUsernameRoute',
            api_id = websocketgw.ref,
            route_key = 'setusername',
            authorization_type = 'NONE',
            operation_name = 'SetUsernameRoute',
            target = 'integrations/' + setusername_integration.ref 
        )
        
        deployment = apiv2.CfnDeployment(self, 'Deployment',
            api_id = websocketgw.ref,
        )
        deployment.add_depends_on(sendmessage_route)
        deployment.add_depends_on(setusername_route)
        deployment.add_depends_on(connect_route)
        deployment.add_depends_on(disconnect_route)
        
        

        stage = apiv2.CfnStage(self, 'stage',
            stage_name= 'prod',
            description= 'prod stage',
            # deployment_id= deployment.ref,
            api_id = websocketgw.ref,
        )

        core.CfnOutput(self,'WebSocketURI',
            value = f'wss://{websocketgw.ref}.execute-api.{self.region}.amazonaws.com/prod',
            description = 'URI of websocket'
        )

        print('WebSocket')

class PipelineAwsTestWebsocketStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        websocket = WebsocketStack(self, 'WebSocket')
