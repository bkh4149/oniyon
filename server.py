import random
from flask import Flask, redirect, url_for, render_template, request,session
from flask_session import Session
#通常クライアント側にデータが保存される（session）、サーバー側に保存する場合が(Session)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def home():
    return redirect('/question', code=302)


@app.route('/question') #questionが飛んできたらプログラムが実行
def q1():
    q1= ["問題1 今月は何月ですか？", "6月:7月:8月:9月:10月:11月:12月", "10月:11月", "説明1"]
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
    session["correct_ans"]=q1[2]
    return render_template('index.html', question="問題1 今月は何月ですか？", choices=result)

@app.route('/answer', methods=['GET']) #answerが飛んできたら下のプログラムが実行
def check_answer():
    correct_ans=session["correct_ans"]
    print("correct_ans=",correct_ans)
    
    #10/15の作業
    #anserの複数の答えを一致させるプログラムを作成する

    # user_choice = request.args.get('choice')
    # print(user_choice)
    # correct_choice = "10月"

    # if user_choice == correct_choice:
    #     return "正解です！"
    # else:
    #     return "不正解です。"



if __name__ == "__main__":
    app.run(debug=True,port=8888)