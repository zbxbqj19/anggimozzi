import urllib.parse
import requests
from bs4 import BeautifulSoup

class WebScraper:
    def scrape_naver_search(self, keyword: str) -> list:
        encoded = urllib.parse.quote(keyword)
        url = f"https://search.naver.com/search.naver?query={encoded}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        results = []
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                titles = soup.select('.news_tit, .api_txt_lines')
                for t in titles[:20]:
                    txt = t.get_text().strip()
                    results.append({
                        "title": txt,
                        "description": txt,
                        "link": t.get('href', '#'),
                        "source": "naver_scrape"
                    })
        except Exception:
            pass
        
        if not results:
            return self._demo_data(keyword)
        return results

    def _demo_data(self, keyword: str) -> list:
        return [
            {"title": f"2026 역대급 히트 아이템 {keyword} 상세 스펙 리뷰", "description": f"소비자 평점 4.9를 달성한 신형 {keyword} 제품군 트렌드 집중 분석 데이터.", "source": "demo"},
            {"title": f"실패 없는 {keyword} 브랜드 가성비 순위 TOP 5", "description": f"요즘 커뮤니티에서 가장 바이럴이 많이 일어나는 {keyword} 솔직 장단점 요약.", "source": "demo"},
            {"title": f"품절 대란 {keyword} 대안 상품 및 직구 가이드", "description": f"가격 대비 훌륭한 퍼포먼스로 인기를 끌고 있는 차세대 {keyword} 트렌드 리포트.", "source": "demo"}
        ]
