import os
from openai import AzureOpenAI

# 마이크 입력
#import sounddevice as sd
#from scipy.io.wavfile import write
from dotenv import load_dotenv
import streamlit as st
from streamlit_audiorecorder import audiorecorder

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


    st.title("🗣️ Streamlit 음성 입력 데모")
    st.markdown("브라우저 마이크를 통해 음성 녹음을 시도합니다.")

    # audiorecorder 컴포넌트를 사용하여 브라우저에서 음성 입력 받기
    # 이 컴포넌트가 녹음을 시작하고 완료되면 오디오 데이터 객체를 반환합니다.
    audio_data = audiorecorder("🎙️ 클릭하여 녹음 시작", "녹음 중... (완료 시 다시 클릭)")

    # 녹음이 완료되면 (데이터의 길이가 0보다 크면) 다음 로직이 실행됩니다.
    if len(audio_data) > 0:
        st.success("✅ 녹음 완료! 데이터를 처리합니다.")
        
        # audiorecorder는 AudioData 객체를 반환하며, .tobytes()를 사용하여 
        # STT API에 전달할 수 있는 WAV 형식의 바이트 스트림으로 변환합니다.
        audio_bytes = audio_data.tobytes()
        
        # ----------------------------------------------------
        # 🚀 WAV 파일 저장 로직 추가
        # ----------------------------------------------------
        WAV_OUTPUT_FILENAME = "files/user_input.wav"
        
        try:
            # 'wb' (write binary) 모드로 파일을 열어 바이트 데이터를 씁니다.
            with open(WAV_OUTPUT_FILENAME, 'wb') as f:
                f.write(audio_bytes)
            
            st.info(f"💾 WAV 파일 저장 완료: '{WAV_OUTPUT_FILENAME}'")
            
            # 파일 다운로드 링크 제공 (선택 사항)
            with open(WAV_OUTPUT_FILENAME, "rb") as file:
                st.download_button(
                    label="녹음 파일 다운로드",
                    data=file,
                    file_name=WAV_OUTPUT_FILENAME,
                    mime="audio/wav"
                )

        except Exception as e:
            st.error(f"❌ 파일 저장 중 오류 발생: {e}")

    with open(WAV_OUTPUT_FILENAME, 'rb') as audio_file:
        transcription = share_client_1.audio.transcriptions.create(
            model = 'whisper',
            language="ko",
            file = audio_file
        )

        return transcription.text


