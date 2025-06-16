# ====================================================================
# 您的互動式輿情分析網站
# 檔案名稱: app.py
# ====================================================================

import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# --- 核心功能函數 ---

# 1. 抓取Google搜尋結果的網頁標題
def scrape_google_titles(query, num_pages=1):
    """根據關鍵字，抓取Google搜尋結果的標題。"""
    st.info(f"🔍 正在搜尋關於「{query}」的網路資訊...")
    all_titles = ""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    for page in range(num_pages):
        url = f"https://www.google.com/search?q={query}&start={page*10}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() # 確保請求成功
            soup = BeautifulSoup(response.text, 'html.parser')
            # 找到所有 h3 標籤，這通常是搜尋結果的標題
            titles = soup.find_all('h3')
            for title in titles:
                all_titles += title.get_text() + " "
        except requests.exceptions.RequestException as e:
            st.error(f"抓取失敗: {e}")
            return "" # 抓取失敗時返回空字串
            
    st.success("✅ 資訊抓取完成！")
    return all_titles

# 2. 產生文字雲
def generate_wordcloud(text):
    """根據文本產生文字雲圖片。"""
    st.info("☁️ 正在生成文字雲...")
    # 使用 jieba 進行中文分詞
    word_list = jieba.cut(text)
    words = " ".join(word_list)

    # 設定中文字體路徑 (請根據您的作業系統調整)
    # Windows: C:/Windows/Fonts/msjh.ttc (微軟正黑體)
    # Mac: /System/Library/Fonts/PingFang.ttc (蘋方)
    # 如果路徑錯誤，文字雲會顯示為方塊
    font_path = 'C:/Windows/Fonts/msjh.ttc' 

    try:
        wordcloud = WordCloud(width=800, 
                              height=400, 
                              background_color='white', 
                              font_path=font_path,
                              collocations=False # 避免重複詞
                             ).generate(words)
    except RuntimeError:
         st.error("找不到中文字體！請確認 `font_path` 的路徑是否正確。")
         return None


    # 使用 matplotlib 顯示圖片
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    st.success("✅ 文字雲生成完畢！")


# 3. 產生情緒分析圖表 (此處為範例)
def generate_sentiment_chart():
    """產生一個範例的互動式圓餅圖。"""
    st.info("📊 正在生成互動式圖表...")
    labels = ['正面/期待', '中性/資訊', '負面/抱怨']
    values = [60, 35, 5] # 範例數據

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text="<b>網路輿情情緒分佈 (範例)</b>")
    st.plotly_chart(fig)
    st.success("✅ 互動式圖表生成完畢！")

# --- 網站介面設計 ---

# 設定網頁標題和圖示
st.set_page_config(page_title="互動式輿情分析儀", page_icon="📈")

# 網站標題
st.title("📈 互動式網路輿情分析儀")
st.write("這是一個簡易的網路輿情分析工具，您可以輸入任何關鍵字，它會自動抓取相關資訊並生成視覺化的文字雲與圖表。")

# 讓使用者輸入關鍵字
query = st.text_input("請輸入您想分析的關鍵字（例如：食尚玩家）", "食尚玩家")

# 分析按鈕
if st.button("🚀 開始分析！"):
    if query:
        # 步驟 1: 抓取資料
        scraped_text = scrape_google_titles(query)
        
        if scraped_text:
            # 顯示抓取到的原始文字摘要
            with st.expander("點此查看抓取到的文字摘要"):
                st.write(scraped_text)
                
            # 步驟 2: 產生文字雲
            generate_wordcloud(scraped_text)
            
            # 步驟 3: 產生互動圖表
            generate_sentiment_chart()

    else:
        st.warning("請先輸入關鍵字！")

st.markdown("---")
st.write("由 Gemini AI 協助開發")