import re
from collections import Counter
from analysis.preprocessor import KoreanPreprocessor

class TrendAnalyzer:
    def __init__(self):
        self.preprocessor = KoreanPreprocessor()

    def analyze_products(self, shopping_items: list) -> dict:
        products = []
        brands = Counter()
        malls = Counter()
        categories = Counter()
        
        for item in shopping_items:
            price_raw = str(item.get("price", "0")).replace(",", "")
            try:
                price = int(price_raw) if price_raw.isdigit() else 0
            except ValueError:
                price = 0
                
            brand = item.get("brand", "미지정")
            if not brand or brand.strip() == "": brand = "미지정"
            
            mall = item.get("mall", "기타")
            category = item.get("category", "기타")
            
            product_info = {
                "title": item.get("title", "").replace("<b>", "").replace("</b>", ""),
                "price": price,
                "brand": brand,
                "mall": mall,
                "category": category
            }
            products.append(product_info)
            
            if brand != "미지정":
                brands[brand] += 1
            malls[mall] += 1
            categories[category] += 1
            
        return {
            "products": products,
            "brands": dict(brands.most_common(10)),
            "malls": dict(malls.most_common(10)),
            "categories": dict(categories.most_common(10))
        }

    def analyze_trend_signals(self, all_items: list, keyword: str) -> dict:
        word_counter = Counter()
        source_counts = Counter()
        
        for item in all_items:
            src = item.get("source", "unknown")
            source_counts[src] += 1
            
            text = f"{item.get('title', '')} {item.get('description', '')}"
            tokens = self.preprocessor.tokenize(text)
            for t in tokens:
                if t != keyword and len(t) > 1:
                    word_counter[t] += 1
                    
        return {
            "word_frequency": dict(word_counter.most_common(30)),
            "source_breakdown": dict(source_counts)
        }

    def extract_product_names(self, all_items: list) -> list:
        names = set()
        # 영어+숫자 조합의 모델명 패턴 정규식 추출
        pattern = re.compile(r'\b[A-Z0-9\-]{3,15}\b')
        for item in all_items:
            text = item.get('title', '')
            matches = pattern.findall(text)
            for m in matches:
                if not m.isdigit() and not m.startswith('-'):
                    names.add(m)
        return list(names)[:15]
