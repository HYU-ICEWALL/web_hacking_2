import os
from flask import Flask, request, render_template, redirect
from models import db, User
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Icewall!'
    
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
            return "회원가입 성공"

    else:
        return render_template("signup.html")

if __name__ == "__main__":
    with app.app_context():
        basedir = os.path.abspath(os.path.dirname(__file__)) # 현재 파일이 있는 폴더 경로
        dbfile = os.path.join(basedir, 'db.sqlite') # 데이터베이스 파일 생성
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        db.app = app
        db.create_all()

        app.run(host="127.0.0.1", port=5000, debug=True)