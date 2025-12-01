######### 이미지 설명
import base64

# pip install python-dotenv
from dotenv import load_dotenv

import os
from openai import AzureOpenAI

# .env 환경변수 로드
load_dotenv()
AZURE_OAI_ENDPOINT = os.getenv("AZURE_OAI_ENDPOINT")
AZURE_OAI_KEY = os.getenv("AZURE_OAI_KEY")
AZURE_OAI_DEPLOYMENT = os.getenv("AZURE_OAI_DEPLOYMENT")
      
client = AzureOpenAI(
    azure_endpoint = AZURE_OAI_ENDPOINT,
    api_key = AZURE_OAI_KEY,
    api_version="2025-01-01-preview"
)


def image_to_text(file_path) :

    # 서버에서 이미지 읽기 위해, 이미지 인코딩
    encoded_image = base64.b64encode(open(file_path, 'rb').read()).decode('ascii')

    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "시각장애인이 음성으로 만든 이미지야. 그에게 이미지에 대해서 객체, 분위기, 색깔, 상황 등 상세한 설명을 부탁해"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "\n"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                },
                {
                    "type": "text",
                    "text": "시각장애인이 음성으로 만든 이미지야. 그에게 이미지에 대해서 객체, 분위기, 색깔, 상황 등 상세한 설명을 부탁해"
                }
            ]
        }
    ]

    # Include speech result if speech is enabled
    messages = chat_prompt

    completion = client.chat.completions.create(
        model=AZURE_OAI_DEPLOYMENT,
        messages=messages,
        max_tokens=300,
        temperature=0.87,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    image_explain_text = completion.choices[0].message.content
    print(f'이미지 분석 텍스트 : {image_explain_text}')
    return image_explain_text