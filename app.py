import os
from flask import Flask, request, render_template, redirect, session
from models import db, User
app = Flask(__name__)

@app.route('/')
def hello():
    if 'username' not in session:
        return redirect('/login/')
    else:
        username = session['username']
        return "Hello, " + username # 로그인 상태라면 username 출력
    
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not(username):
            return "사용자 이름이 입력되지 않았습니다"
        else:
            usertable=User()
            usertable.username = username
            usertable.password = password

            db.session.add(usertable)
            db.session.commit()
            return redirect('/')

    else:
        return render_template("signup.html")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # print(username) -> 터미널창에서 username 확인 가능, 디버깅 시 사용

        if not(username and password):
            return "입력되지 않은 정보가 있습니다"
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    session['username'] = username
                    return redirect('/')
                else:
                    return "비밀번호가 다릅니다"
            else:
                return "사용자가 존재하지 않습니다"
    else:
        return render_template('login.html')
if __name__ == "__main__":
    with app.app_context():
        basedir = os.path.abspath(os.path.dirname(__file__)) # 현재 파일이 있는 폴더 경로
        dbfile = os.path.join(basedir, 'db.sqlite') # 데이터베이스 파일 생성

        app.config['SECRET_KEY'] = "ICEWALL" # 세션관리 및 암호화를 위한 시크릿키 생성
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        db.app = app
        db.create_all()

        app.run(host="127.0.0.1", port=5000, debug=True)