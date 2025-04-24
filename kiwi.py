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
columns = ['title', 'channel', 'description', 'view_count']
df = pd.read_csv('/home/ubuntu/damf2/yootube/data/2025-04-23.csv', names=columns, header=0, encoding='utf-8')
df['title'] = df['title'].apply(clean_title) # 제목에 불용어 없애기
df['tokens'] = df['title'].apply(tokenize_and_remove_stopwords) # 불용어 제거 및 형태소 분석

# # 확인
for i in range(2):
    print(f"{i}번:\n원문: {df['title'][i]}\n토큰: {df['tokens'][i]}\n")