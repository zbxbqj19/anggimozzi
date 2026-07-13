import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from analysis.preprocessor import KoreanPreprocessor

class TfidfAnalyzer:
    def __init__(self, max_features=100):
        self.preprocessor = KoreanPreprocessor()
        self.max_features = max_features
        # Scikit-learn Vectorizer에 Kiwi 토크나이저 바인딩
        self.vectorizer = TfidfVectorizer(
            tokenizer=self.preprocessor.tokenize,
            lowercase=True,
            max_features=self.max_features
        )

    def analyze(self, documents: list) -> dict:
        if not documents or all(not str(d).strip() for d in documents):
            return {"keywords": []}
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            feature_names = self.vectorizer.get_feature_names_out()
            # 모든 문서에서 해당 키워드의 TF-IDF 스코어 합산 계산
            scores = tfidf_matrix.sum(axis=0).A1
            
            df = pd.DataFrame({'keyword': feature_names, 'score': scores})
            df = df.sort_values(by='score', ascending=False)
            
            keywords = [{"word": row['keyword'], "score": round(float(row['score']), 4)} for _, row in df.iterrows()]
            return {"keywords": keywords}
        except Exception:
            # 빈 매트릭스 등으로 오류 발생 시 빈도수 기반 폴백 처리
            word_counts = {}
            for doc in documents:
                for token in self.preprocessor.tokenize(str(doc)):
                    word_counts[token] = word_counts.get(token, 0) + 1
            sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
            return {"keywords": [{"word": k, "score": float(v)} for k, v in sorted_words[:self.max_features]]}

    def compare_keywords(self, doc_groups: dict) -> dict:
        comparison = {}
        for source, docs in doc_groups.items():
            if docs and len([d for d in docs if str(d).strip()]) > 0:
                res = self.analyze(docs)
                comparison[source] = res["keywords"][:10]
            else:
                comparison[source] = []
        return comparison
