
##### 사용자 음성 녹음 텍스트 => 이미지 변환
import json
import requests
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

# .env 환경변수 로드
load_dotenv()
AZURE_CHRIS_KEY = os.getenv("AZURE_CHRIS_KEY")
OTHER_KEY = os.getenv("OTHER_KEY")


# 이러한 환경 변수를 설정하거나 다음 값을 편집해야 합니다.
endpoint = "https://el22-mieta6ou-australiaeast.cognitiveservices.azure.com/"
api_version = "2024-04-01-preview"
deployment = "dall-e-3"
api_key = OTHER_KEY

share_client_2 = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key,
)

def text_to_image(user_input_text) :
    print(f'사용자 입력 텍스트 : {user_input_text}')
    result = share_client_2.images.generate(
        model=deployment,
        prompt=user_input_text,
        n=1,
        style="vivid",
        quality="standard",
    )

    # 서버에 저장된 이미지 URL
    image_url = json.loads(result.model_dump_json())['data'][0]['url']

    # 이미지 요청 
    response_img = requests.get(image_url)
    file_path = 'files/ai_output_image.jpg'

    # 이미지 저장
    with open(f'{file_path}', 'wb') as f :
        f.write(response_img.content)

    return file_path


