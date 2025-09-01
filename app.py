from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

app = Flask(__name__)

# Gemini APIの設定
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        concern = data.get('concern', '')
        
        if not concern:
            return jsonify({'error': '悩みを入力してください'}), 400
        
        # Geminiに相談内容を送信
        prompt = f"""あなたは優しく親身になって相談に乗るカウンセラーです。
以下の悩みに対して、温かく支援的なアドバイスを日本語で提供してください。

相談内容: {concern}

回答は以下の形式でお願いします：
1. 具体的で実践的なアドバイスを2-3個提供する
2. 前向きな励ましの言葉で締めくくる"""
        
        response = model.generate_content(prompt)
        
        return jsonify({'response': response.text})
    
    except Exception as e:
        print(f"Error: {str(e)}")  # エラーログを出力
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)