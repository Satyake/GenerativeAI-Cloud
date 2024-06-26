from langchain.llms.bedrock import Bedrock
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import boto3

print('ok')
bedrock_client=boto3.client(
    service_name="bedrock-runtime",region_name='us-east-1'

)

model_id='ai21.j2-ultra-v1'
llm=Bedrock(
    model_id=model_id,
    client=bedrock_client
    
)

def mymodel(user_prompt):
    prompt=PromptTemplate(
        input_variables=['user_prompt'],
        template="You are a chatbot. Provide answer for {user_prompt}"
    )
    bedrock_chain=LLMChain(llm=llm, prompt=prompt)
    response=bedrock_chain({'user_prompt': user_prompt})
    return response

user_prompt='what is python?'
res=mymodel(user_prompt)
print(res['text'])