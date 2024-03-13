# 텍스트 요약을 위한 모듈

import openai
import os
import tiktoken

def load_api_key(file_path):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

# OpenAI 라이브러리를 이용해 텍스트를 요약하는 함수
def summarize_text(user_text, lang="en"): # lang 인자에 영어를 기본적으로 지정
    
    API_KEY_PATH = 'C:\\Users\\bluecom010\\Desktop\\지의\\24_03_06_프로젝트\\OpenAI_API.txt'
    openai.api_key = load_api_key(API_KEY_PATH)
    
    # API 키 설정
    # openai.api_key = os.environ["OPENAI_API_KEY"]

    # 대화 메시지 정의
    if lang == "en":
        messages = [ 
            {"role": "system", "content": "You are a helpful assistant in the summary."},
            {"role": "user", "content": f"Summarize the following. \n {user_text}"}
        ]
    elif lang == "ko":
        messages = [ 
            {"role": "system", "content": "You are a helpful assistant in the summary."},
            {"role": "user", "content": f"다음의 내용을 한국어로 요약해 주세요 \n {user_text}"}
#             {"role": "user", "content": f"Summarize the following in Korea. \n {user_text}"}
        ]
        
    # Chat Completions API 호출
    response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", # 사용할 모델 선택 
                            messages=messages, # 전달할 메시지 지정
                            max_tokens=2000,  # 응답 최대 토큰 수 지정 
                            temperature=0.3,  # 완성의 다양성을 조절하는 온도 설정
                            n=1              # 생성할 완성의 개수 지정
    )     
    summary = response["choices"][0]["message"]["content"]
    return summary

# 요약 리스트를 최종적으로 요약하는 함수
def summarize_text_final(text_list, lang = 'en'):
    # 리스트를 연결해 하나의 요약 문자열로 통합
    joined_summary = " ".join(text_list) 

    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_num = len(enc.encode(joined_summary)) # 텍스트 문자열의 토큰 개수 구하기

    req_max_token = 2000 # 응답을 고려해 설정한 최대 요청 토큰    
    final_summary = "" # 빈 문자열로 초기화
    if token_num < req_max_token: # 설정한 토큰보다 작을 때만 실행 가능
        # 하나로 통합한 요약문을 다시 요약
        final_summary = summarize_text(joined_summary, lang)
        
    return token_num, final_summary