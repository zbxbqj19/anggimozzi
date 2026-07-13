import requests
from config import Config

class GoogleCollector:
    def __init__(self):
        self.api_key = Config.GOOGLE_API_KEY
        self.cse_id = Config.GOOGLE_CSE_ID

    def search(self, keyword: str) -> list:
        if not self.api_key or not self.cse_id:
            return []
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": keyword,
            "num": min(Config.MAX_RESULTS_PER_SOURCE, 10)
        }
        try:
            res = requests.get(url, params=params, timeout=10)
            if res.status_code == 200:
                data = res.json()
                items = data.get("items", [])
                return [{
                    "title": item.get("title", ""),
                    "description": item.get("snippet", ""),
                    "link": item.get("link", ""),
                    "source": "google"
                } for item in items]
        except Exception:
            pass
        return []
