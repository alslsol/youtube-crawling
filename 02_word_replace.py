from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from konlpy.tag import Okt
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

# 형태소 분석 + 불용어 제거 함수 (konlpy 사용)
def tokenize_and_remove_stopwords(text):
    okt = Okt()
    stopwords = set([
        '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를',
        '으로', '자', '에', '와', '한', '하다', '에서', '부터', '까지', '고', '도'
    ])
    tokens = okt.morphs(text, stem=True)
    filtered_tokens = [token for token in tokens if token not in stopwords]
    return filtered_tokens

# 3. CSV 파일 로드 및 처리
df = pd.read_csv('/home/ubuntu/damf2/yootube/data/2025-04-24.csv', encoding='utf-8')
# print(df.columns)

# 4. 제목 정제 및 토큰화 적용
df['title'] = df['title'].apply(clean_title)
df['tokens'] = df['title'].apply(tokenize_and_remove_stopwords)

# 5. 확인
for i in range(5):
    print(f"{i}번:\n원문: {df['title'][i]}\n토큰: {df['tokens'][i]}\n")
    print(f"{i}번:\n원문: {df['description'][i]}\n토큰: {df['tokens'][i]}\n")