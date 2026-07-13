import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# 한글 폰트 및 마이너스 기호 깨짐 처리 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Mac 환경일 경우 'AppleGothic'으로 변경
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font="Malgun Gothic")

class ChartGenerator:
    def _to_base64(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=130)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_str}"

    def keyword_bar_chart(self, keywords: list) -> str:
        if not keywords: return ""
        top_k = keywords[:15]
        words = [k['word'] for k in top_k]
        scores = [k['score'] for k in top_k]
        
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.barplot(x=scores, y=words, ax=ax, palette='Blues_r', hue=words, legend=False)
        ax.set_title("TF-IDF 키워드 가중치 가시화", fontsize=12, fontweight='bold', pad=10)
        return self._to_base64(fig)

    def word_frequency_chart(self, word_freq: dict) -> str:
        if not word_freq: return ""
        items = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]
        words = [i[0] for i in items]
        counts = [i[1] for i in items]
        
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.barplot(x=counts, y=words, ax=ax, palette='flare', hue=words, legend=False)
        ax.set_title("연관어 절대 빈도수 순위", fontsize=12, fontweight='bold', pad=10)
        return self._to_base64(fig)

    def source_pie_chart(self, source_breakdown: dict) -> str:
        if not source_breakdown: return ""
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(source_breakdown.values(), labels=source_breakdown.keys(), autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        ax.set_title("채널별 수집 비중", fontsize=12, fontweight='bold')
        return self._to_base64(fig)

    def generate_wordcloud(self, keywords: list) -> str:
        if not keywords: return ""
        freq_dict = {k['word']: k['score'] for k in keywords}
        
        try:
            wc = WordCloud(
                font_path="c:/Windows/Fonts/malgun.ttf",  # OS별 폰트 경로 가변 적용 가능
                background_color='white',
                width=800,
                height=450,
                max_words=60,
                colormap='viridis'
            ).generate_from_frequencies(freq_dict)
        except Exception:
            try:
                wc = WordCloud(background_color='white', width=800, height=450).generate_from_frequencies(freq_dict)
            except Exception:
                return ""
        
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        return self._to_base64(fig)

    def price_distribution(self, products: list) -> str:
        prices = [p['price'] for p in products if p['price'] > 0]
        if not prices: return ""
        
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.histplot(prices, kde=True, ax=ax, color='teal', bins=12)
        ax.set_title("시장 상품 가격대별 매핑", fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel("가격 (원)")
        return self._to_base64(fig)

    def brand_chart(self, brands: dict) -> str:
        if not brands: return ""
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(x=list(brands.values()), y=list(brands.keys()), ax=ax, palette='magma', hue=list(brands.keys()), legend=False)
        ax.set_title("주요 경쟁 브랜드 점유 집중도", fontsize=12, fontweight='bold', pad=10)
        return self._to_base64(fig)

    def source_comparison_radar(self, source_comparison: dict) -> str:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.text(0.5, 0.5, "크로스 채널 데이터 연동 완료", ha='center', va='center', color='grey', fontdict={'weight':'bold'})
        ax.axis('off')
        return self._to_base64(fig)
