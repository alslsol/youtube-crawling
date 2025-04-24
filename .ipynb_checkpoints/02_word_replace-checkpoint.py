from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
import pandas as pd
import re

# 1. 제목의 쉼표, 이모티콘, 특수문자 등 삭제
def clean_title(text):
    text = str(text)
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)  # 이모지 제거
    text = text.replace(',', '')                         # 쉼표 제거
    text = re.sub(r'[^\w\s]', '', text)                  # 특수문자 제거
    text = text.strip()                                  # 앞뒤 공백 제거
    return text

# 2. Kiwi 형태소 분석기
def tokenize_and_remove_stopwords(text):
    kiwi = Kiwi()  # Kiwi 형태소 분석기 객체 생성
    stopwords = Stopwords()
    filtered_tokens = kiwi.tokenize(text=text, stopwords=stopwords)
    return filtered_tokens


#     # 토큰화
#     tokens = kiwi.tokenize(text)
#     # 불용어 제거: 형태소만 추출
#     filtered_tokens = [token.form for token in tokens if token.form not in stopwords]
#     return filtered_tokens

# # csv 파일 읽기
columns = ['date', 'title', 'channel', 'view_count']
df = pd.read_csv('/home/ubuntu/damf2/yootube/data/2025-04-23.csv', names=columns, header=0)
df = df.drop('date', axis=1)
df['title'] = df['title'].apply(clean_title) # 제목에 불용어 없애기
df['tokens'] = df['title'].apply(tokenize_and_remove_stopwords) # 불용어 제거 및 형태소 분석

# # 확인
for i in range(2):
    print(f"{i}번:\n원문: {df['title'][i]}\n토큰: {df['tokens'][i]}\n")