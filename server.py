import random
from flask import Flask, redirect, url_for, render_template, request,session
from flask_session import Session
#通常クライアント側にデータが保存される（session）、サーバー側に保存する場合が(Session)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

sets = [
    ["問題1 今月は何月ですか？", "6月:7月:8月:9月:10月:11月:12月", "10月", "説明1"],
    ["問題2 以下の動物の中で鳥はどれ？", "ライオン:象:ペンギン:カンガルー:カモメ:スズメ", "ペンギン:カモメ:スズメ", "ペンギンは鳥の一種ですが、飛べません。"],
    ["問題3 最も大きな惑星は？", "地球:火星:木星:金星", "木星", "木星は太陽系で最も大きな惑星です。"],
    ["問題4 日本の首都は？", "大阪:東京:福岡:仙台", "東京", "日本の首都は東京です。"],
    ["問題5 以下の中で果物はどれ？", "ピーマン:キャベツ:ブロッコリー:メロン:パイナップル:バナナ", "メロン:パイナップル:バナナ", "メロン:パイナップル:バナナは果物の一種ですが、野菜としても扱われることが多いです。"],
    ["問題6 以下の言語の中でスペイン語で「こんにちは」は？", "Hello:Bonjour:Halo:Hola", "Hola", "スペイン語で「こんにちは」は「Hola」と言います。"],
]


@app.route('/')
def home():
    session["q_no"] = 0
    return redirect('/question', code=302)

@app.route('/question') #questionが飛んできたらプログラムが実行
def q1():
    q_no=session["q_no"]
    q1= sets[q_no]
    print(q1[0])  # 質問文の表示

    arr = q1[1].split(":")  # 解答群の作成　多数の中から４つをランダムで選択
    print("arr=",arr)
    if len(arr) < 4:
        crs = len(arr)
    else:
        crs = 4    
    result = random.sample(arr, crs)
    
    for i, choice in enumerate(result, 1):
        print(i, choice)

    #正解をここで作ってセッションに保存しておく
    #answer側ではこれと比較するだけで良いようにしておく
    cs_temp = set(q1[2].split(":"))
    correct_choices = set(result) & cs_temp
    session["correct_ans"] = correct_choices

    return render_template('index.html', question=q1[0], choices=result)

@app.route('/answer', methods=['GET']) #answerが飛んできたら下のプログラムが実行
def check_answer():
    correct_ans=session["correct_ans"]
    print("correct_ans=",correct_ans)
    
    #10/15の作業
    #anserの複数の答えを一致させるプログラムを作成する
    user_choice = request.args.getlist('choice[]')  
    print("user_choice=",user_choice)

    #q_noをプラス
    q_no = session["q_no"]
    q_no = q_no+1
    session["q_no"]=q_no

    if set(user_choice) == correct_ans:
        kekka="正解です！"
    else:
        kekka="不正解です。"
    return render_template('kekka.html', kekka=kekka, q_no=q_no )


if __name__ == "__main__":
    app.run(debug=True,port=8888)