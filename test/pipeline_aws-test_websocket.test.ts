import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as PipelineAwsTestWebsocket from '../lib/pipeline_aws-test_websocket-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new PipelineAwsTestWebsocket.PipelineAwsTestWebsocketStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
