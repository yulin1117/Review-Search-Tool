
import requests
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import jieba.posseg as pseg

# 使用者輸入關鍵字
keyword = input("請輸入關鍵字:")
# 設定要爬取的頁數
pages = int(input("請輸入要爬取的頁數:"))

# 設定請求標頭，模擬瀏覽器請求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 儲存文章內容的字串
text_data = ''

# 逐頁爬取文章
for page in range(1, pages+1):
    # PTT搜尋頁面URL
    url = f"https://www.ptt.cc/bbs/BeautySalon/search?page={page}&q={keyword}"

    # 發送GET請求
    response = requests.get(url, headers=headers)

    # 使用BeautifulSoup解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到文章列表的元素
    articles = soup.find_all('div', class_='r-ent')

    # 逐個處理文章
    for article in articles:
        # 找到文章內容鏈結元素
        link_element = article.find('a')
        if link_element is not None:
            # 獲取文章內容鏈結
            link = 'https://www.ptt.cc' + link_element.get('href')
            # 發送GET請求獲取文章內容
            article_response = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            # 找到所有留言元素
            content_elements = article_soup.find_all(
                "span", class_="f3 push-content")

            for content_element in content_elements:
                # 獲取留言內容文字
                content = content_element.text.encode('utf-8').decode('utf-8')
                # 儲存留言內容
                text_data += content

# 過濾無意義字元
removeword = ['span', 'class', 'f3', 'https', 'imgur', 'h1', '_   blank', 'href', 'rel', 'nofollow', 'target', 'cdn', 'cgi', 'b4', 'jpg', 'hl', 'b1', 'f5', 'f4', 'goo.gl', 'f2', 'email', 'map', 'f1', 'f6', '__cf___', 'data', 'bbs', 'html', 'cf', 'f0', 'b2', 'b3', 'b5', 'b6', '原文內容', '原文連結', '作者', '標題', '時間', '看板', '<', '>', '，',
              '。', '?', '—', '我', '喜歡', '很', '是', '的', '也', '但', '有', '就', '跟', '用', '用過', '買', '感覺', '沒', '之前', '嗎', '比較', '你', '最近', '錯', '要', '而且', '啊', '有', '好', '都', '不', '會', '可以', '不會', '閒聊', '感謝', '用心', '了', '推薦', '原po', '真的', '會啊', '分享', '錯版', '笑死', '愛用', '好用', '覺得', '個人', '伸手', '・', '/', '=', '\"', '\n', '」', '「', '！', '[', ']', '：', '‧', '╦', '╔', '╗', '║', '╠', '╬', '╬', ':', '╰', '╩', '╯', '╭', '╮', '│', '╪', '─', '《', '》', '_', '.', '、', '（', '）', '　', '*', '※', '~', '○', '”', '“', '～', '@', '＋', '\r', '▁', ')', '(', '', '═', '?', ',', '!', '…', '&', ';', '『', '』', '#', '＝', '\l']

for word in removeword:
    text_data = text_data.replace(word, '')
text_data = re.sub(r'X+D+|哈+|推+|謝+', '', text_data)


# 使用jieba進行關鍵詞提取
tfidf_fre = jieba.analyse.extract_tags(
    text_data, topK=200, withWeight=True, allowPOS=(), withFlag=True)

# 把分析完的詞頻輸出成字典
count_dic = {}

for word, weight in tfidf_fre:
    words = jieba.posseg.cut(word)
    for w, f in words:
        if f.startswith('n') or f.startswith('eng'):  # 只保留名詞
            count_dic[w] = weight


print(count_dic)


# 生成文字雲
font_path = "/Users/yulin/Desktop/程式/源雲明體GenWanMin TW TTF SemiBold.ttf"
wordcloud = WordCloud(width=1600, height=800,
                      background_color='white', font_path=font_path).fit_words(count_dic)


# 繪製文字雲
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

# 保存文字雲圖片到指定資料夾
output_path = "/Users/yulin/Desktop/程式/文字雲.png"
wordcloud.to_file(output_path)
