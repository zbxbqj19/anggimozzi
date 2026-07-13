import requests
from config import Config

class NaverCollector:
    def __init__(self):
        self.client_id = Config.NAVER_CLIENT_ID
        self.client_secret = Config.NAVER_CLIENT_SECRET

    def _get_headers(self):
        return {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
            "Content-Type": "application/json"
        }

    def _call_api(self, target: str, keyword: str) -> list:
        url = f"https://openapi.naver.com/v1/search/{target}.json"
        params = {
            "query": keyword,
            "display": min(Config.MAX_RESULTS_PER_SOURCE, 50)
        }
        try:
            res = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
            if res.status_code == 200:
                return res.json().get("items", [])
        except Exception:
            pass
        return []

    def search_all(self, keyword: str) -> dict:
        blog_raw = self._call_api("blog", keyword)
        news_raw = self._call_api("news", keyword)
        shop_raw = self._call_api("shop", keyword)

        return {
            "blog": [{"title": i.get("title", ""), "description": i.get("description", ""), "link": i.get("link", ""), "source": "naver_blog"} for i in blog_raw],
            "news": [{"title": i.get("title", ""), "description": i.get("description", ""), "link": i.get("link", ""), "source": "naver_news"} for i in news_raw],
            "shopping": [{
                "title": i.get("title", ""),
                "price": i.get("lprice", "0"),
                "brand": i.get("brand", "미지정"),
                "mall": i.get("mallName", "기타"),
                "category": f"{i.get('category1','')}/{i.get('category2','')}",
                "link": i.get("link", ""),
                "description": f"브랜드: {i.get('brand','')}, 몰: {i.get('mallName','')}",
                "source": "naver_shopping"
            } for i in shop_raw]
        }

    def search_shopping(self, keyword: str) -> list:
        return self.search_all(keyword)["shopping"]
