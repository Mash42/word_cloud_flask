from flask import Flask, render_template, request
import pymysql
import requests
import re
from flask import Markup
import MeCab
from wordcloud import WordCloud

app = Flask(__name__)

# ホーム
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

# ワードクラウド作成
@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        input_text = request.form['input_text']
        #　ワードクラウド作成
        create_cloud(input_text)
        return render_template("result.html")
    
    return render_template("index.html")



def create_cloud(texts):
    word_list = []
    print('あ')
    tagger = MeCab.Tagger('-Ochasen')
    print('い')
    texts_line = texts.split('\n')
    for text in texts_line:
        node = tagger.parseToNode(text)
        while node:
            if node.feature.split(',')[0] == '名詞':
                word_list.append(node.surface)
            node = node.next

    input_texts = ' '.join(word_list)
    output_image = WordCloud(
        #font_path='/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
        background_color="white",
        width=900, height=900,
        max_words=500,
        min_font_size=4,
        collocations=False
    ).generate(input_texts)
    output_image.to_file('.\static\img\wordcloud.png')

# アプリ起動
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
