#!/usr/bin/env python3

from aws_cdk import core

from pipeline_aws_test_websocket.pipeline_aws_test_websocket_stack import PipelineAwsTestWebsocketStack


app = core.App()
PipelineAwsTestWebsocketStack(app, "pipeline-aws-test-websocket")

app.synth()
