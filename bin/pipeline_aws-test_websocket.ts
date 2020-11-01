#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { PipelineAwsTestWebsocketStack } from '../lib/pipeline_aws-test_websocket-stack';

const app = new cdk.App();
new PipelineAwsTestWebsocketStack(app, 'PipelineAwsTestWebsocketStack');
