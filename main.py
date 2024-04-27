import flask_login
from flask import Flask, redirect, render_template, jsonify, make_response
from data import db_session
from data.users import User
from data.courses import Course
from data.lessons import Lesson
from data.tasks import Task
from flask_login import LoginManager, login_user, logout_user, login_required
from data.forms.login import LoginForm
from data.forms.task import TaskForm
from data.forms.register import RegisterForm
from data.forms.course import CourseForm\

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Gdagdegdagdagdo'

login_manager = LoginManager()
login_manager.init_app(app)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.completed_courses = ' '
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/teach')
def teach():
    return render_template('teach.html')


@app.route('/learn', methods=['GET'])
def learn():
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


@app.route('/learn/<string:course_name>')
@login_required
def course(course_name):
    course, lesson, lessons = get_data(course_name, None)
    is_course_completed = True
    for lsn in lessons:
        if str(flask_login.current_user.id) not in lsn.completed_by_users:
            is_course_completed = False

    db_session.global_init('database.db')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == flask_login.current_user.id).first()
    if is_course_completed:
        user.completed_courses += f'{course.id}'
    else:
        user.completed_courses.replace(f'{course.id}', '')
        tmp = list(user.completed_courses).copy()
        for i in tmp:
            if i == str(course.id):
                tmp.remove(i)
        user.completed_courses = ''.join(tmp)
    db_sess.commit()

    return render_template('course.html', course=course, lessons=lessons)


@app.route('/learn/<string:course_name>/<string:lesson_id_in_course>')
@login_required
def lesson(course_name, lesson_id_in_course):
    course, lesson, lessons = get_data(course_name, lesson_id_in_course)
    return render_template('lesson.html', lesson=lesson, course=course, lessons=lessons)

def get_data(course_name, lesson_id_in_course):
    course, lesson, lessons = None, None, None
    db_session.global_init('database.db')
    db_sess = db_session.create_session()
    if course_name:
        course = db_sess.query(Course).filter(Course.name == course_name).first()
    if lesson_id_in_course:
        lesson = db_sess.query(Lesson).filter(Lesson.id_in_course == lesson_id_in_course and Lesson.course_id == course.id).first()

    lessons = db_sess.query(Lesson).filter(Lesson.course_id == course.id).all()
    return course, lesson, lessons


@app.route('/learn/<string:course_name>/<int:lesson_id_in_course>/theory')
@login_required
def theory(course_name, lesson_id_in_course):
    course, lesson, lessons = get_data(course_name, lesson_id_in_course)
    return render_template('theory.html', lesson=lesson, course=course, lessons=lessons)


@app.route('/learn/<string:course_name>/<int:lesson_id_in_course>/tasks')
@login_required
def tasks(course_name, lesson_id_in_course):
    db_session.global_init('database.db')
    db_sess = db_session.create_session()
    course, lesson, lessons = get_data(course_name, lesson_id_in_course)
    tasks = db_sess.query(Task).filter(Task.lesson_id == lesson.id).all()
    is_all_complete = True
    for task in tasks:
        if str(flask_login.current_user.id) not in task.users_passed:
            is_all_complete = False
    if is_all_complete:
        lesson = db_sess.query(Lesson).filter(Lesson.id_in_course == lesson_id_in_course and Lesson.course_id == course.id).first()
        lesson.completed_by_users += f'{flask_login.current_user.id}'
    else:
        lesson = db_sess.query(Lesson).filter(Lesson.id_in_course == lesson_id_in_course and Lesson.course_id == course.id).first()
        if str(flask_login.current_user.id) in lesson.completed_by_users:
            lesson.completed_by_users.replace(str(flask_login.current_user.id), '')
    lesson = db_sess.query(Lesson).filter(Lesson.id_in_course == lesson_id_in_course and Lesson.course_id == course.id).first()
    db_sess.commit()

    return render_template('list_of_tasks.html', lesson=lesson, course=course, lessons=lessons, tasks=tasks)


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

@app.route('/learn/<string:course_name>/<int:lesson_id_in_course>/tasks/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task(course_name, lesson_id_in_course, task_id):
    course, lesson, lessons = get_data(course_name, lesson_id_in_course)

    db_session.global_init('database.db')
    db_sess = db_session.create_session()
    next_id = lesson.id_in_course + 1
    next_lesson = db_sess.query(Lesson).filter(Lesson.id_in_course == next_id, course.id == Lesson.course_id).first()
    tasks = db_sess.query(Task).filter(Task.lesson_id == lesson.id).all()
    form = TaskForm()
    lesson = db_sess.query(Lesson).filter(Lesson.id_in_course == lesson_id_in_course).first()
    task = db_sess.query(Task).filter(Task.id_in_lesson == task_id, lesson.id == Task.lesson_id).first()
    if form.validate_on_submit():
        user_passed = task.users_passed
        task.users_passed = user_passed + f'{flask_login.current_user.id}'
        db_sess.commit()
        db_sess = db_session.create_session()
        lesson = db_sess.query(Lesson).filter(Lesson.id_in_course == lesson_id_in_course).first()
        tasks = db_sess.query(Task).filter(Task.lesson_id == lesson.id).all()
        is_all_complete = True
        for task in tasks:
            if str(flask_login.current_user.id) not in task.users_passed:
                is_all_complete = False
        if is_all_complete:
            lesson = db_sess.query(Lesson).filter(
                Lesson.id_in_course == lesson_id_in_course, Lesson.course_id == course.id).first()
            lesson.completed_by_users += f'{flask_login.current_user.id}'
        else:
            lesson = db_sess.query(Lesson).filter(
                Lesson.id_in_course == lesson_id_in_course, Lesson.course_id == course.id).first()
            if str(flask_login.current_user.id) in lesson.completed_by_users:
                lesson.completed_by_users.replace(str(flask_login.current_user.id), '')
        lesson = db_sess.query(Lesson).filter(
            Lesson.id_in_course == lesson_id_in_course, Lesson.course_id == course.id).first()
        db_sess.commit()
        return redirect(f'/learn/{course_name}/{lesson_id_in_course}/tasks/{task_id}')


    return render_template('task.html', lesson=lesson,
                           course=course, lessons=lessons, tasks=tasks, task=task, task_id=task_id,
                           db_sess=db_sess, form=form, next_lesson=next_lesson)


@app.route('/teach/new', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        course = Course()
        course.name = form.name.data
        course.description = form.description.data
        course.user_id = flask_login.current_user.id
        db_sess.add(course)
        db_sess.commit()
        return redirect('/teach/my-courses')
    return render_template('new.html', form=form)


@app.route('/')
def main_page():
    return render_template('main.html', title='ГЛАВНАЯ СТРАНИЦА')

@app.route('/teach/my-courses')
@login_required
def my_courses():
    db_sess = db_session.create_session()
    my_courses = db_sess.query(Course).filter(Course.user_id == flask_login.current_user.id)
    users = db_sess.query(User).all()
    return render_template('my_courses.html', my_courses=my_courses, users=users)

@app.route('/teach/<string:course_name>', methods=['GET', 'POST'])
@login_required
def edit(course_name):
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.name == course_name).first()
    return render_template('edit_course.html', course=course)


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
