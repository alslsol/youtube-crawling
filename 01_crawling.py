# 인급동 제목, 조회수 크롤링

from googleapiclient.discovery import build
from dotenv import load_dotenv
from datetime import datetime
import os
import csv
import re

# 유튜브 API 키
load_dotenv()
# 환경변수에서 API 키 읽기
API_KEY = os.getenv('YOUTUBE_KEY')

# 유튜브 API 클라이언트 빌드
youtube = build('youtube', 'v3', developerKey=API_KEY)


def clean_text(text):
    text = re.sub(r'http\S+|www\.\S+', '', text)  # http 또는 www 로 시작하는 모든 링크 제거
    # 이모티콘 제거 (유니코드 범위 기반)
    text = re.sub(r'[^\w\s.,!?()가-힣ㄱ-ㅎㅏ-ㅣ]', '', text)
    # 줄바꿈, 캐리지리턴 제거
    text = text.replace('\n', ' ').replace('\r', ' ')
    # 쉼표 제거 (CSV 구분자와 충돌 방지용)
    text = text.replace(',', ' ')
    return text.strip()


# 인기급상승 영상 가져오기
def get_trending_videos(region_code='KR', max_results=50):
    request = youtube.videos().list(
        part='snippet,statistics',
        chart='mostPopular',
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()

    video_data = []
    for item in response['items']:
        channel = clean_text(item['snippet']['channelTitle'])
        view_count = int(item['statistics']['viewCount'])
        title = clean_text(item['snippet']['title'])
        description = clean_text(item['snippet'].get('description', '')) # 설명란
        video_data.append({
            'channel': channel,
            'view_count': view_count,
            'title': title,
            'description': description
        })    
    return video_data

# 5. csv 파일 저장 함수
local_dir = '/home/ubuntu/damf2/yootube/data'
today = datetime.today().strftime('%Y-%m-%d')
file_path = os.path.join(local_dir, f'{today}.csv')


def save_to_csv(data):
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['channel', 'view_count', 'title', 'description'])
        writer.writeheader()        # 헤더 추가
        writer.writerows(data)      # 딕셔너리 리스트 저장
    print(f'✅ 데이터 저장 완료: {file_path}')

if __name__ == '__main__':
    video_data = get_trending_videos()
    save_to_csv(video_data)