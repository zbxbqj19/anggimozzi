import os
import re
from kiwipiepy import Kiwi
from config import Config

class KoreanPreprocessor:
    def __init__(self):
        self.kiwi = Kiwi()
        self.stopwords = set()
        self._load_stopwords()

    def _load_stopwords(self):
        # 기본 내장 불용어 정의
        default_stopwords = [
            '그리고', '하지만', '그러나', '그래서', '내개', '우리', '저희', '때문', '경우', 
            '대한', '통해', '위해', '대해', '관련', '이후', '최근', '올해', '지난', '이번', 
            '통한', '또한', '대하여', '모든', '통해', '통하여', '정말', '진짜', '너무'
        ]
        self.stopwords.update(default_stopwords)
        
        # 파일이 존재하면 추가 로드
        if os.path.exists(Config.STOPWORDS_PATH):
            try:
                with open(Config.STOPWORDS_PATH, 'r', encoding='utf-8') as f:
                    for line in f:
                        w = line.strip()
                        if w and not w.startswith('#'):
                            self.stopwords.add(w)
            except Exception:
                pass

    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', ' ', text)
        # URL 제거
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        # 한글, 영문, 숫자, 공백을 제외한 모든 특수문자 제거
        text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
        return text

    def tokenize(self, text: str) -> list:
        cleaned = self.clean_text(text)
        if not cleaned.strip():
            return []
        
        tokens = []
        try:
            # Kiwi 분석기를 통한 명사(NNG: 일반명사, NNP: 고유명사) 추출
            res = self.kiwi.tokenize(cleaned)
            for token in res:
                if token.tag in ['NNG', 'NNP']:
                    word = token.form
                    # 최소 단어 길이 조건 충족 및 불용어 제외
                    if len(word) >= Config.MIN_WORD_LENGTH and word not in self.stopwords:
                        tokens.append(word)
        except Exception:
            # 형태소 분석 에러 시 공백 기준 스플릿 폴백
            tokens = [w for w in cleaned.split() if len(w) >= Config.MIN_WORD_LENGTH and w not in self.stopwords]
        return tokens
