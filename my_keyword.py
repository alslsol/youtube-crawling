# 키워드 분석, 텍스트 마이닝: 이건 아직 실행도 안 했음, gpt만 돌려서 작성한 코드임

import csv
import os
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from collections import Counter
import re

# NLTK의 불용어 다운로드 (처음 한 번만)
nltk.download('stopwords')

# 파일 경로 (csv에서 데이터를 불러오기 위한 경로)
file_path = '/home/ubuntu/damf2/yootube/data/2025-04-23.csv'

# 텍스트 전처리 함수 (소문자화 + 특수문자 제거)
def preprocess_text(text):
    text = text.lower()  # 소문자화
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # 알파벳과 공백만 남기기
    return text

# 키워드 분석 (단어 빈도 계산)
def analyze_keywords(video_data):
    # 모든 제목 합치기
    titles = ' '.join([video['title'] for video in video_data])

    # 텍스트 전처리
    processed_titles = preprocess_text(titles)

    # 불용어(stop words) 설정
    stop_words = set(stopwords.words('english'))

    # 단어 리스트로 변환
    words = processed_titles.split()

    # 불용어 제거한 단어들만 필터링
    filtered_words = [word for word in words if word not in stop_words]

    # 단어 빈도 계산 (Counter 사용)
    word_freq = Counter(filtered_words)

    # 상위 10개 키워드 출력
    print(f"상위 10개 키워드:")
    for word, freq in word_freq.most_common(10):
        print(f"{word}: {freq}")

    return filtered_words

# 워드 클라우드 생성
def create_wordcloud(filtered_words):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_words))

    # 워드클라우드 시각화
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 축 표시 안 함
    plt.show()

# CSV 파일에서 데이터 읽어오기
def read_video_data_from_csv(file_path):
    video_data = []
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            video_data.append({
                'title': row['title'],
                'channel': row['channel'],
                'view_count': row['view_count']
            })
    return video_data

# 실행
if __name__ == '__main__':
    # 1. CSV 파일에서 데이터 읽기
    video_data = read_video_data_from_csv(file_path)

    # 2. 키워드 분석
    filtered_words = analyze_keywords(video_data)

    # 3. 워드 클라우드 시각화
    create_wordcloud(filtered_words)
