from kiwi import Kiwi
from collections import Counter
import os
import pandas as pd

# Kiwi 초기화
kiwi = Kiwi()

# 고유명사 목록
custom_exceptions = [
    '강찬석', '지박령', '김규남', '인스타', '유튜브', '오즈모', '주현영', '남중규', '서수민',
    '프로모션', '프로야구', '훈남', '글로스', '투어스', '속마음'
]

# 분석할 품사 (일반명사, 고유명사)
allowed_pos = {'NNG', 'NNP'}

# 불용어 목록
custom_stopwords = set([
    '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를',
    '으로', '자', '에', '와', '한', '하다', '에서', '부터', '까지', '고',
    '입니다', '그리고', '그', '것', '수', '또한', '있는', '없는', '(', ')', '.',
    '!', '?', '글', '오늘', '영상', '지금', '문의', '감사', 'ㅜㅜ', 'ㅠㅠ', 'ㅋㅋ',
    '링크', '인', '스타', '투', '유', '제작', '참여', '이벤트', '김', '전', '사용',
])

# 고유명사 보호용 언더스코어 붙이기
def preserve_proper_nouns(text, proper_nouns):
    if not isinstance(text, str):
        text = str(text) if isinstance(text, float) else ''
    for phrase in proper_nouns:
        text = text.replace(phrase, phrase + "_")
    return text

# 고유명사 병합 처리
def merge_proper_nouns(result, custom_exceptions):
    merged = []
    for token in result:
        word, tag = token.form, token.tag
        if word.endswith("_"):  # 보호된 고유명사
            merged.append((word[:-1], 'NNP'))
        elif word in custom_exceptions:
            merged.append((word, 'NNP'))
        else:
            merged.append((word, tag))
    return merged

# 형태소 분석 함수
def analyze_morphology(sentence):
    try:
        analyzed = kiwi.analyze(sentence)[0][0]  # 첫 번째 결과만 사용
        filtered = [token for token in analyzed if token.tag in allowed_pos]
        return filtered
    except Exception as e:
        print(f"형태소 분석 오류: {e}")
        return []

# 파일 불러오기
def get_file_list():
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    return os.listdir(data_folder) if os.path.exists(data_folder) else []

def csv_to_dataframe(file_name):
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    file_path = os.path.join(data_folder, file_name)
    if not os.path.exists(file_path): return None
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"CSV 읽기 오류: {e}")
        return None

def get_column_as_list(df, col_name):
    return df[col_name].tolist() if col_name in df.columns else []

# ✅ 메인 분석 실행
if __name__ == "__main__":
    file_list = get_file_list()
    total_tokens = []

    for file_name in file_list:
        print(f"Processing: {file_name}")
        df = csv_to_dataframe(file_name)
        if df is None: continue

        titles = get_column_as_list(df, 'title')
        descriptions = get_column_as_list(df, 'description')

        for text in titles + descriptions:
            print(f"Analyzing: {text}")
            text = preserve_proper_nouns(text, custom_exceptions)
            tokens = analyze_morphology(text)
            merged = merge_proper_nouns(tokens, custom_exceptions)

            words = [
                word for word, pos in merged
                if word not in custom_stopwords
            ]
            total_tokens.extend(words)

    # 빈도수 출력
    freq = Counter(total_tokens)
    print("\n📊 자주 등장한 단어 Top 20:")
    for word, count in freq.most_common(20):
        print(f"{word}: {count}회")