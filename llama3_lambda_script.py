import json
import boto3
import botocore.config
import datetime
def content_generate_bedrock_llama3(blogtopic):
    prompt=f""" <s> [INST] Human: Write a 200
    word blog on the topic {blogtopic}
    Assistant:[/INST]
    """ 
    body={
        "prompt":prompt,
        "max_gen_len":512,
        "temperature":0.5,
        "top_p":0.9
    }

    try:
        bedrock=boto3.client('bedrock-runtime',
                             region_name='us-east-1', 
                             config=botocore.config.Config(
                                 read_timeout=300,
                                 retries={'max_attempts':3}))
        response=bedrock.invoke_model(
            body=json.dumps(body),
            modelId='meta.llama3-8b-instruct-v1:0',
    
        )
        response_content=response.get('body').read()
        response_data=json.loads(response_content)
        print(response_data)

        blog_details=response_data['generation']
        return blog_details
    except Exception as e:
        print(f"Error generating the blog : {e}")
        return ""
        


#upload content to s3
def s3_uploader(s3_key, s3_bucket, generate_blog):
    s3=boto3.client('s3')
    try:
        s3.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=generate_blog
        ) 
        print("Data is saved in S3")
    except Exception as e:
        print(f"Error uploading data to S3: {e}")



def lambda_handler(event, context):
    event=json.loads(event['body'])
    blogtopic=event['blogtopic']
    generate_blog=content_generate_bedrock_llama3(blogtopic)

    if generate_blog:
        current_time=datetime.datetime.now().strftime('%H%M%S')
        s3_key=f"blog-output/{current_time}.txt"
        s3_bucket="awsbedrockapp0099"
        s3_uploader(s3_key,s3_bucket,generate_blog)
    else:
        print("Failed to generate blog content")

    return {
        'statusCode': 200,
        'body': json.dumps('Response generated ')
    }

