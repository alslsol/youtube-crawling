from konlpy.tag import Kkma
from konlpy.utils import pprint
from collections import Counter
import os
import pandas as pd

# 고유명사 목록
custom_exceptions = [
    '강찬석', '지박령', '김규남', '인스타', '유튜브', '오즈모', '주현영', '남중규', '서수민',
    '프로모션', '프로야구', '훈남', '글로스', '투어스', '속마음'
]

# 추출할 품사
allowed_pos = {'NNG', 'NNP'}

# 불용어 목록
custom_stopwords = set([
    '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를',
    '으로', '자', '에', '와', '한', '하다', '에서', '부터', '까지', '고', '도',
    '입니다', '그리고', '그', '것', '수', '또한', '있는', '없는', '(', ')', '.',
    '!', '?', '글', '오늘', '영상', '지금', '문의', '감사', 'ㅜㅜ', 'ㅠㅠ', 'ㅋㅋ',
    '링크', '인', '스타', '투', '유', '제작', '참여', '이벤트', '김', '전', '사용',
])

# 고유명사 보호 함수
def preserve_proper_nouns(text, proper_nouns):
    if not isinstance(text, str):
        text = str(text) if isinstance(text, float) else ''  # float 타입은 str로 변환, 그 외는 빈 문자열로 처리

    # 고유명사에 _ 넣어서 보호
    for phrase in proper_nouns:
        if phrase in text:
            text = text.replace(phrase, phrase + "_")
    return text

# def restore_proper_nouns(tokens):
#     # NaN 처리 및 문자열로 변환
#     if not isinstance(text, str):
#         text = str(text) if isinstance(text, float) else ''  # float 타입은 str로 변환, 그 외는 빈 문자열로 처리

#     for phrase in proper_nouns:
#         if phrase in text:
#             text = text.replace(phrase, phrase.replace(" ", "_"))
#     return text

def get_file_list():
    """
    파일 목록을 가져오는 함수
    
    :return: 파일 목록 (list of strings)
    """
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    
    if not os.path.exists(data_folder):
        print(f"'{data_folder}' 폴더가 존재하지 않습니다.")
        return []
    
    # 파일 목록 읽기
    file_list = os.listdir(data_folder)
    return file_list


def csv_to_dataframe(file_name):
    """
    :param file_name: CSV 파일 이름 (string)

    :return: DataFrame (pandas DataFrame)
    """

    # 'data' 폴더 경로 설정
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    file_path = os.path.join(data_folder, file_name)
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        print(f"'{file_path}' 파일이 존재하지 않습니다.")
        return None
    
    # CSV 파일을 DataFrame으로 읽기
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None


def get_column_as_list(dataframe, column_name):
    """
    :param dataframe DataFrame (pandas DataFrame)
    :param column_name 컬럼 이름 (string)

    :return: 컬럼 값 리스트 (list)
    """
    if column_name not in dataframe.columns:
        print(f"'{column_name}' 컬럼이 DataFrame에 존재하지 않습니다.")
        return []
    
    # 컬럼 값을 리스트로 변환
    return dataframe[column_name].tolist()

# 고유어 합치는 함수
def merge_proper_nouns(result, allowed_pos, custom_exceptions):
    """
    고유명사를 하나의 토큰으로 합치는 함수
    :param result: 형태소 분석 결과 (list of tuples)
    :param allowed_pos: 분석할 품사 (set)
    :return: 하나로 합쳐진 토큰 리스트
    """
    merged_words = []
    current_word = ""
    current_pos = ""
    
    for word, pos in result:
        # 고유명사 연속이 있으면 하나로 합침
        if word in custom_exceptions:
            if current_word == "":
                current_word = word  # 새로운 단어 시작
                current_pos = pos
            else:
                current_word += word  # 연속된 고유명사 합치기
        else:
            # 고유명사 연속이 끝났으면 기존 단어를 저장하고 초기화
            if current_word:
                merged_words.append((current_word, current_pos))
                current_word = ""
                current_pos = ""
            if word != "_":  # 보호된 고유명사 "_"는 제외하고 추가
                merged_words.append((word, pos))  # 고유명사 외의 다른 품사는 그대로 추가
        
    # 마지막에 남아 있는 단어 추가
    if current_word:
        merged_words.append((current_word, current_pos))
    
    return merged_words


def analyze_morphology(sentence):
    """
    문장을 입력받아 형태소 분석 결과를 반환하는 함수
    :param sentence 분석할 문장 (string)

    :return: 형태소 분석 결과 (list of tuples)
    """
    kkma = Kkma()
    try:
        result = kkma.pos(sentence)
        result = [word_pos for word_pos in result if word_pos[1] in allowed_pos]
        return result
    except Exception as e:
        print(f"형태소 분석 중 오류가 발생했습니다: {e}")
        return []


if __name__ == "__main__":
    # 파일 목록 가져오기
    file_list = get_file_list()
    total_tokens = []

    for file_name in file_list:
        print(f"Processing file: {file_name}")
        df = csv_to_dataframe(file_name)

        titles = get_column_as_list(df, 'title')
        descriptions = get_column_as_list(df, 'description')
        
        for title in titles:
            # print(f"Analyzing title: {title}")

            # 고유명사 보호
            title = preserve_proper_nouns(title, custom_exceptions)

            # 형태소 분석
            result = analyze_morphology(title)

            # 고유명사 합치기
            merged_words = merge_proper_nouns(result, allowed_pos, custom_exceptions)
            
            words = [
                word if word.endswith('_') else word.replace('_', '') # 고유명사 토큰은 유지
                for word, pos in merged_words 
                if word.replace('_', '') not in custom_stopwords]
            total_tokens.extend(words)
            # print(merged_words)

        for description in descriptions:
            # print(f"Analyzing description: {description}")

            # 고유명사 보호
            description = preserve_proper_nouns(description, custom_exceptions)

            result = analyze_morphology(description)
            
            # 고유명사 합치기
            merged_words = merge_proper_nouns(result, allowed_pos, custom_exceptions)
            
            words = [
                word if word.endswith('_') else word.replace('_', '')
                for word, pos in merged_words
                if word.replace('_', '') not in custom_stopwords]
            total_tokens.extend(words)
            # print(merged_words)

# 빈도 계산
freq = Counter(total_tokens)
print("\n📊 자주 등장한 단어 Top 20:")
for word, count in freq.most_common(20):
    print(f"{word}: {count}회")

# tf-idf
total_docs = []

for file_name in file_list:
    print(f"Processing file: {file_name}")
    df = csv_to_dataframe(file_name)

    titles = get_column_as_list(df, 'title')
    descriptions = get_column_as_list(df, 'description')

    for title, description in zip(titles, descriptions):
        # --- 문서 하나 만들기 ---
        tokens = []

        for text in [title, description]:
            text = preserve_proper_nouns(text, custom_exceptions)
            result = analyze_morphology(text)
            merged_words = merge_proper_nouns(result, allowed_pos, custom_exceptions)
            words = [
                word if word.endswith('_') else word.replace('_', '')
                for word, pos in merged_words
                if word.replace('_', '') not in custom_stopwords
            ]
            tokens.extend(words)

        total_docs.append(tokens)  # 하나의 문서 완성!


# 분석
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt

# TF-IDF 입력을 위해 "문장"으로 변환
docs_as_str = [" ".join(doc) for doc in total_docs]

# 벡터화
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs_as_str)
feature_names = vectorizer.get_feature_names_out()

# 상위 키워드 추출
tfidf_scores = tfidf_matrix.sum(axis=0).A1
sorted_indices = np.argsort(tfidf_scores)[::-1]
top_n = 20
top_keywords = [(feature_names[i], tfidf_scores[i]) for i in sorted_indices[:top_n]]

# 결과 출력
print("\n🔑 TF-IDF 상위 키워드 Top 20:")
for word, score in top_keywords:
    print(f"{word}: {score:.4f}")

# 시각화
# keywords, scores = zip(*top_keywords)
# plt.figure(figsize=(10, 6))
# plt.barh(keywords[::-1], scores[::-1], color='coral')
# plt.title("Top 20 Keywords by TF-IDF Score")
# plt.xlabel("TF-IDF Score")
# plt.tight_layout()
# plt.show()