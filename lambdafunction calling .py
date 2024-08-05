import json
import boto3
ENDPOINT="huggingface-pytorch-tgi-inference-2024-08-05-15-43-08-720"
sagemaker_runtime=boto3.client(
    "sagemaker-runtime", region_name='us-east-1')


def lambda_handler(event, context):
    query_params=event['queryStringParameters']
    query=query_params.get('query')
    payload={
    'inputs':query,
    'parameters':{
    'max_new_tokens':256,
    'do_sample':True,
    'temperature':0.3,
    'top_p':0.4,
    'top_k':50,
    'repitition_penalty' :1.03
    }}
    response=sagemaker_runtime.invoke_endpoint(
    EndpointName=ENDPOINT,
    ContentType="application/json",
    Body=json.dumps(payload))
    predictions=json.loads(response['Body'].read().decode('utf-8'))
    final_result=predictions[0]['generated_text']
    return {
        'statusCode': 200,
        'body': json.dumps(final_result)
    }
