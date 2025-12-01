import os
import tempfile # 임시 파일 사용을 위해 추가
from openai import AzureOpenAI

# .env 환경변수 로드
from dotenv import load_dotenv
import streamlit as st


# audiorecorder가 streamlit_audiorecorder에서 import 된다고 가정하고,
# 모듈을 찾지 못할 경우에 대비한 예외 처리를 추가합니다.
try:
    from audiorecorder import audiorecorder
except ImportError:
    st.error("❌ 'streamlit-audiorecorder' 모듈을 찾을 수 없습니다. 음성 입력 기능이 작동하지 않습니다.")
    # audiorecorder 함수를 임시로 정의하여 ImportError를 방지
    def audiorecorder(*args, **kwargs): return []

# .env 환경변수 로드
load_dotenv()
AZURE_CHRIS_KEY = os.getenv("AZURE_CHRIS_KEY")
OTHER_KEY = os.getenv("OTHER_KEY")
     
# Azure OpenAI 클라이언트 초기화
share_client_1 = AzureOpenAI(
    api_key=AZURE_CHRIS_KEY,
    api_version="2024-06-01",
    azure_endpoint = 'https://8a000-openai.openai.azure.com/'
)

def user_input() :
    """
    Streamlit UI를 통해 사용자 음성 녹음을 처리하고 STT를 수행합니다.
    (함수 호출 시 UI가 표시되며, 사용자가 클릭하여 녹음을 시작/종료해야 합니다.)
    """
    transcribed_text = None

    st.title("🗣️ Streamlit 음성 입력 데모")
    st.markdown("이미지를 설명할 음성을 녹음해 주세요. 녹음 버튼을 클릭하면 시작됩니다.")
    
    # audiorecorder 컴포넌트를 사용하여 브라우저에서 음성 입력 받기
    audio_data = audiorecorder("🎙️ 클릭하여 녹음 시작", "녹음 중... (완료 시 다시 클릭)")

    
    # ----------------------------------------------------
    # 녹음이 완료되면 (데이터의 길이가 0보다 크면) 다음 로직이 즉시 실행됩니다.
    # ----------------------------------------------------
    if len(audio_data) > 0:
        st.success("✅ 녹음 완료! 데이터를 처리합니다.")
        
        # 오디오 데이터를 바이트 스트림으로 변환
        audio_bytes = audio_data.tobytes()
        
        # 임시 파일 경로를 초기화합니다.
        temp_audio_path = None
        
        try:
            # 1. 임시 파일 생성 및 바이트 데이터 쓰기 (WAV 파일 저장 로직)
            # tempfile을 사용하여 안전하게 파일을 생성하고 경로를 얻습니다.
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_bytes)
                temp_audio_path = tmp_file.name # 임시 파일 경로 저장
            
            st.info(f"💾 WAV 임시 파일 생성 완료")

            # 2. STT API 호출
            with open(temp_audio_path, 'rb') as audio_file:
                transcription = share_client_1.audio.transcriptions.create(
                    model = 'whisper',
                    language="ko",
                    file = audio_file
                )
                transcribed_text = transcription.text
            
            # 3. 파일 다운로드 링크 제공
            WAV_OUTPUT_FILENAME = "files/user_input.wav" # 다운로드 시 사용자에게 보여줄 이름
            with open(temp_audio_path, "rb") as file:
                st.download_button(
                    label="녹음 파일 다운로드",
                    data=file,
                    file_name=WAV_OUTPUT_FILENAME,
                    mime="audio/wav"
                )

        except Exception as e:
            st.error(f"❌ 파일 처리 또는 STT 중 오류 발생: {e}")
            transcribed_text = "음성 변환 실패"

        finally:
            # 4. 임시 파일 정리
            if temp_audio_path and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
        
        st.subheader("📝 변환된 텍스트:")
        st.markdown(f"**{transcribed_text}**")
        
        return transcribed_text
    
    # 녹음 데이터가 없거나 오류 발생 시 None 반환
    return None
