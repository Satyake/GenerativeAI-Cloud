import json 
import requests 
import openai 
from openai import AzureOpenAI 

def main():
    api_key="0b1000355ccc498db8c6a5d8b31d8494"
    endpoint="https://azstudiows09x.openai.azure.com/"
    client=AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version="2024-05-01-preview"
    )

    functions=[

        {
            "name": "getweather", 
            "description": "Retrieve the real time weather", 
            'parameters': {
                "type":"object",
                "properties": {
                    "location":{
                        "type":"string",
                        "description":" the exact location whose real-time weather is to be determined",

                    },
                },
                    "required":["location"]

                }
            }
        
        
    ]

    completion=client.chat.completions.create(
        model='gpt-35-turbo', 
        messages=[
            {
                "role": "system",
                "content": "Your an expert in retrieving real time weather data/info" 
                },
            { 
                "role": "user",
                "content": "What is the weather in mumbai?"
            }
        ], functions=functions
    )
    function_argument=completion.choices[0].message.function_call.arguments
    print(function_argument)
    #location=function_argument['location']
    #if location: 
    #    print(f"city:{location}")
    
    #response=completion
    #print(response.choices[0].message.content)
    #print(response)

if __name__ == "__main__":
    main()