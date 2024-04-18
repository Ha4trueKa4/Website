from flask import Flask, redirect, render_template, jsonify, make_response
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, logout_user, login_required
from data.forms.login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ODINDVATRI'

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

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/register')
def logout():
    return


@app.route('/')
def main_page():
    return render_template('base.html', title='ГЛАВНАЯ СТРАНИЦА')

def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
