import pygame
import time
import os
import user_input
import text_to_image
import image_to_text
import text_to_audio

guide_file_relative = r"files/guide.mp3"

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

guide_file_absolute = os.path.join(script_dir, guide_file_relative)

# 파일 존재 여부 검사
if not os.path.exists(guide_file_absolute):
    print(f"❌ 오류: 파일을 찾을 수 없습니다.")
    print(f"  검사된 경로: {guide_file_absolute}")
else:
    try:
        # 1. Pygame 초기화
        pygame.init()
        
        # 2. Pygame 믹서 초기화 (오디오 시스템 설정)
        pygame.mixer.init()
        
        # 3. 오디오 파일 로드
        pygame.mixer.music.load(guide_file_absolute)
        
        # 4. 재생 시작
        print(f"'{guide_file_absolute}' 파일을 재생합니다...")
        pygame.mixer.music.play()
        
        # 5. 재생이 끝날 때까지 대기
        # get_busy()는 음악이 재생 중인지 확인합니다.
        while pygame.mixer.music.get_busy():
            time.sleep(1)
            
        print("재생이 완료되었습니다.")
        
    except pygame.error as e:
        # Pygame 관련 오류 (예: 파일 형식 문제, 믹서 초기화 실패)
        print("\n❌ 재생 실패: Pygame 오류 발생!")
        print(f"  오류 내용: {e}")
    finally:
        # Pygame 종료
        pygame.quit()

# 사용자 이미지 음성 입력 텍스트
user_input_text = user_input.user_input()

# 사용자 입력 텍스트 => 이미지 변환
file_path =  text_to_image.text_to_image(user_input_text)

# 이미지 설명 텍스트 추출
image_to_text = image_to_text.image_to_text(file_path)

# 이미지 설명 텍스트 => 음성 변환
audio_file_path = text_to_audio.text_to_audio(image_to_text)


audio_file_relative = rf"{audio_file_path}"

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

audio_file_absolute = os.path.join(script_dir, audio_file_relative)

# 파일 존재 여부 검사
if not os.path.exists(audio_file_absolute):
    print(f"❌ 오류: 파일을 찾을 수 없습니다.")
    print(f"  검사된 경로: {audio_file_absolute}")
else:
    try:
        # 1. Pygame 초기화
        pygame.init()
        
        # 2. Pygame 믹서 초기화 (오디오 시스템 설정)
        pygame.mixer.init()
        
        # 3. 오디오 파일 로드
        pygame.mixer.music.load(audio_file_absolute)
        
        # 4. 재생 시작
        print(f"'{audio_file_absolute}' 파일을 재생합니다...")
        pygame.mixer.music.play()
        
        # 5. 재생이 끝날 때까지 대기
        # get_busy()는 음악이 재생 중인지 확인합니다.
        while pygame.mixer.music.get_busy():
            time.sleep(1)
            
        print("재생이 완료되었습니다.")
        
    except pygame.error as e:
        # Pygame 관련 오류 (예: 파일 형식 문제, 믹서 초기화 실패)
        print("\n❌ 재생 실패: Pygame 오류 발생!")
        print(f"  오류 내용: {e}")
    finally:
        # Pygame 종료
        pygame.quit()