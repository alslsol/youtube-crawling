from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from konlpy.tag import Okt
from pprint import pprint
import pandas as pd
import re
import csv

# 1. 제목의 쉼표, 이모티콘, 특수문자 등 삭제
def clean_title(text):
    text = str(text)
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)  # 이모지 제거
    text = text.replace(',', '')                         # 쉼표 제거
    text = re.sub(r'[^\w\s]', '', text)                  # 특수문자 제거
    text = text.strip()                                  # 앞뒤 공백 제거
    return text


# 고유어 사전
custom_exceptions = [
    '강찬석', '지박령', '삼성전자', '서울특별시', '카카오엔터프라이즈', 'TV조선', '채널A'
]
def preserve_phrases(text, phrase_list):
    for phrase in phrase_list:
        if phrase in text:
            text = text.replace(phrase, phrase.replace(' ', '_'))  # 띄어쓰기 있는 경우도 대비
    return text

# 형태소 분석 + 불용어 제거 함수 (konlpy 사용)
def tokenize_and_remove_stopwords(text):
    okt = Okt()
    stopwords = set([
        '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를',
        '으로', '자', '에', '와', '한', '하다', '에서', '부터', '까지', '고', '도',
        '에게', '그리고', '그', '것', '로', 'ㅋㅋ', 'ㅠㅠ', '그래도', '너무', '어느',
        '제', '죠', '을'
    ])
    text = preserve_phrases(text, custom_exceptions)
    tokens = okt.morphs(text, stem=True)
    tokens = [token.replace('_', '') for token in tokens]
    filtered_tokens = [token for token in tokens if token not in stopwords]
    return filtered_tokens

# 읽기 및 처리
with open('/home/ubuntu/damf2/yootube/data/2025-04-24.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader):
        raw_title = row['title']
        cleaned_title = clean_title(raw_title)
        tokens_title = tokenize_and_remove_stopwords(cleaned_title)
    
        raw_description = row['description']
        cleaned_description = clean_title(raw_description)
        tokens_description = tokenize_and_remove_stopwords(cleaned_description)

        print(f"📌\n[{i+1}번 제목]")
        print(f"원문: {raw_title}")
        print(f"정제: {cleaned_title}")
        print(f"토큰: {tokens_title}")
        print(f"📌\n[{i+1}번 설명]")
        print(f"원문: {raw_description}")
        print(f"정제: {cleaned_description}")
        print(f"토큰: {tokens_description}")
        print('----------------')

# 3. CSV 파일 로드 및 처리
# df = pd.read_csv('/home/ubuntu/damf2/yootube/data/2025-04-24.csv', encoding='utf-8')
# # print(df.columns)

# # 4. 제목 정제 및 토큰화 적용
# df['title'] = df['title'].apply(clean_title)
# df['tokens'] = df['title'].apply(tokenize_and_remove_stopwords)

# print(df['tokens'].head(2))

# # 5. csv 파일 저장 함수
# local_dir = '/home/ubuntu/damf2/yootube/data'
# today = datetime.today().strftime('%Y-%m-%d')
# file_path = os.path.join(local_dir, f'{today}.csv')

# # 아직 하는 중
# def save_to_csv(data):
#     with open(file_path, 'w', encoding='utf-8-sig', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=['channel', 'view_count', 'title', 'description'])
#         writer.writeheader()        # 헤더 추가
#         writer.writerows(data)     # 딕셔너리 리스트 저장
#     print(f'✅ 데이터 저장 완료: {file_path}')

# if __name__ == '__main__':
#     video_data = get_trending_videos()
#     save_to_csv(video_data)

# 5. 확인
# for i in range(5):
#     print(f"{i}번:\n원문: {df['title'][i]}\n토큰: {df['tokens'][i]}\n")
#     print(f"{i}번:\n원문: {df['description'][i]}\n토큰: {df['tokens'][i]}\n")