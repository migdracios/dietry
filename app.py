# 라이브러리
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

# 앱 셋업
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # SQLite 데이터베이스를 사용하고 있습니다. 필요에 따라 변경하세요.
db = SQLAlchemy(app)

# 운동 데이터 모델 설계
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    name = db.Column(db.String(50))
    activity = db.Column(db.String(50))
    calories = db.Column(db.String(50))
    bpm = db.Column(db.String(50))

# 시작화면 - 운동 데이터 보여주기
@app.route('/')
def render_index():
    exercises = Exercise.query.order_by(desc(Exercise.date)).all()  # date 열을 기준으로 내림차순 정렬합니다.
    return render_template('index.html', exercises=exercises)

# 운동 데이터 삽입
@app.route('/add_exercise', methods=["POST"])
def add_excercise():
    date = request.form.get('date')
    name = request.form.get('name')
    activity = request.form.get('activity')
    calories = request.form.get('calories')
    bpm = request.form.get('bpm')

    new_exercise = Exercise(date=date, name=name, activity=activity, calories=calories, bpm=bpm)
    db.session.add(new_exercise)
    db.session.commit()

    return redirect(url_for('render_index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True, port=8080)