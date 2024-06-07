from flask import Flask, render_template, request
from openai import OpenAI
import PyPDF2

USE_LangChain = True

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_pdf():
    # フォームからPDFファイルを取得
    pdf_file = request.files['pdf_file']
    
    # PDFファイルを読み込む
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    #USE_LangChain https://zenn.dev/pipon_tech_blog/articles/08f959bab19c97

    # ChatGPTに送信
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたは口調がタメ口で、高圧的な上司です。怒りレベルはMAX"},
            {"role": "user", "content": f"以下の部下の作った資料を読み、上司としてダメな点を2点指摘してください。誤字脱字、体裁は指摘しない。：\n\n{text}"}
        ]
    )
    
    # ChatGPTからの返答を取得
    response_text = completion.choices[0].message.content
    
    return render_template('index.html', response=response_text)

if __name__ == '__main__':
    app.run(debug=True)
