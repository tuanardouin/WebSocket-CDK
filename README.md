
# WebSocket CDK Python

This is a basic implementation of websockets using CDK

It's based on the work of [simple-websockets-chat-app](https://github.com/aws-samples/simple-websockets-chat-app) and [@mrpackethead](https://github.com/mrpackethead)

## Install

```
$ python3 -m venv .venv
```

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

If you're using CDK for the first time in your account don't forget to initialize it.

## Deployment

```
$ cdk deploy
```

After the completion of this command go in the API Gateway Console and deploy the API.

## Usage

```
npm install wscat
```

### Deploy API

On AWS console
- Go to API Gateway
- Click on Resources
- Select "deploy API" option on Action menu.

### Connection

```
wscat -c wss://YOUR_API_ID.execute-api.eu-west-1.amazonaws.com/prod
```

### Set username

```
{"action":"setusername", "data":"user1"}
```

### Send message
```
{"action":"sendmessage", "data":"hello world"}
```
