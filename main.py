from flask import Flask, redirect, render_template, jsonify, make_response
from data import db_session
from data.users import User
from data.courses import Course
from flask_login import LoginManager, login_user, logout_user, login_required
from data.forms.login import LoginForm
from data.forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Gdagdegdagdagdo'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/learn', methods=['GET'])
def show_courses():
    db_session.global_init('database.db')
    db_sess = db_session.create_session()
    courses = db_sess.query(Course).all()
    users = db_sess.query(User).all()
    return render_template('list_of_courses.html', courses=courses, users=users)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def main_page():
    return render_template('main.html', title='ГЛАВНАЯ СТРАНИЦА')

def test():
    user = User()
    user.name = "DEAN"
    user.email = 'k@gmail.com'
    user.set_password('12345')
    user.completed_courses = ' '
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

def main():
    db_session.global_init("db/database.db")

    app.run()


if __name__ == '__main__':
    main()
