import os
from openai import AzureOpenAI

# 마이크 입력
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv

# .env 환경변수 로드
load_dotenv()
AZURE_CHRIS_KEY = os.getenv("AZURE_CHRIS_KEY")
OTHER_KEY = os.getenv("OTHER_KEY")
    
share_client_1 = AzureOpenAI(
    api_key=AZURE_CHRIS_KEY,
    api_version="2024-06-01",
    azure_endpoint = 'https://8a000-openai.openai.azure.com/'
)

def user_input() :
    ##### 사용자 음성 녹음

    print("사용자 녹음 시작...")
    second = 5 # 녹음 시간
    user_input_audio_path = 'files/user_input.wav'
    audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()  # 녹음 끝날 때까지 대기
    write(user_input_audio_path, 16000, audio)
    print("사용자 녹음 종료...")

    with open(user_input_audio_path, 'rb') as audio_file:
        transcription = share_client_1.audio.transcriptions.create(
            model = 'whisper',
            language="ko",
            file = audio_file
        )

        return transcription.text