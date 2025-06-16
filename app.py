# ====================================================================
# 您的互動式輿情分析網站 (升級版 v2.0)
# 檔案名稱: app.py
# ====================================================================

import streamlit as st
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# --- 核心功能函數 ---

# 1. 產生文字雲 (功能不變)
def generate_wordcloud(text):
    """根據文本產生文字雲圖片。"""
    st.info("☁️ 正在生成文字雲...")
    word_list = jieba.cut(text)
    words = " ".join(word_list)
    font_path = 'C:/Windows/Fonts/msjh.ttc' 

    try:
        wordcloud = WordCloud(width=800, 
                              height=400, 
                              background_color='white', 
                              font_path=font_path,
                              collocations=False
                             ).generate(words)
    except Exception as e:
         # 在雲端主機上，我們用一個更通用的方式處理字體
         # 如果上面的字體失敗，它會嘗試用預設字體，但可能不支持中文
         st.warning(f"中文字體載入可能失敗，錯誤訊息: {e}。文字雲可能無法正確顯示中文。")
         wordcloud = WordCloud(width=800, height=400, background_color='white').generate(words)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    st.success("✅ 文字雲生成完畢！")


# 2. 產生情緒分析圖表 (功能不變)
def generate_sentiment_chart():
    """產生一個範例的互動式圓餅圖。"""
    st.info("📊 正在生成互動式圖表...")
    labels = ['正面/期待', '中性/資訊', '負面/抱怨']
    values = [60, 35, 5] 

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text="<b>網路輿情情緒分佈 (範例)</b>")
    st.plotly_chart(fig)
    st.success("✅ 互動式圖表生成完畢！")

# --- 網站介面設計 (升級版) ---

st.set_page_config(page_title="貼上即分析儀", page_icon="📋")

st.title("📋 貼上即分析・輿情儀表板")
st.write("這是一個升級版的分析工具。請將您從任何地方（新聞、社群、論壇）複製的文字內容，直接貼到下面的文字框中，即可立即進行分析！")

# 將文字輸入框，升級為更大的文字區域
analyzed_text = st.text_area("請將您想分析的文章、新聞或留言內容貼在此處：", "這裡可以貼上很長的文字...", height=250)

if st.button("🚀 開始分析！"):
    if analyzed_text and analyzed_text != "這裡可以貼上很長的文字...":
        # 直接對貼上的文字進行分析
        st.subheader("分析結果")
        generate_wordcloud(analyzed_text)
        generate_sentiment_chart()
    else:
        st.warning("請先貼上您想分析的文字內容！")

st.markdown("---")
st.write("由 Gemini AI 協助開發 (v2.0)")
