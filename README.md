
# WebSocket CDK Python

This is a basic implementation of websockets using CDK

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