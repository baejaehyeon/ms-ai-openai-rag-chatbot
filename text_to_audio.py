###### 이미지 설명 텍스트 음성 저장
# pip install python-dotenv
from dotenv import load_dotenv

import os
from openai import AzureOpenAI

AZURE_CHRIS_KEY = os.getenv("AZURE_CHRIS_KEY")
OTHER_KEY = os.getenv("OTHER_KEY")

share_client_1 = AzureOpenAI(
    azure_endpoint='https://8a000-openai.openai.azure.com/',
    api_key=AZURE_CHRIS_KEY,
    api_version="2025-03-01-preview",
)

def text_to_audio(image_text) :
    response = share_client_1.audio.speech.create(
        input = image_text,
        model = 'gpt-4o-mini-tts',
        voice= 'shimmer'
    )
    
    response.write_to_file('files/image_explain_text.mp3')

    # 음성 출력
    return "files/image_explain_text.mp3"