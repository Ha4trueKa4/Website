import flask
from flask import jsonify, make_response, request
from data import db_session
from data.courses import Course
from requests import get, post


blueprint = flask.Blueprint(
    'course_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/courses')
def get_courses():
    db_sess = db_session.create_session()
    courses = db_sess.query(Course).all()
    return jsonify(
        {
            'courses':
                [item.to_dict(only=('name', 'description'))
                 for item in courses]
        }
    )
@blueprint.route('/api/courses/<int:course_id>', methods=['GET'])
def get_one_course(course_id):
    db_sess = db_session.create_session()
    courses = db_sess.query(Course).get(course_id)
    if not courses:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'courses': courses.to_dict(only=(
                'name', 'description', 'user_id'))
        }
    )


@blueprint.route('/api/courses', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'description', 'user_id']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    courses = Course(
        name=request.json['title'],
        description=request.json['content'],
        user_id=request.json['user_id']
    )
    db_sess.add(Course)
    db_sess.commit()
    return jsonify({'id': courses.id})


@blueprint.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_news(course_id):
    db_sess = db_session.create_session()
    courses = db_sess.query(Course).get(course_id)
    if not courses:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(courses)
    db_sess.commit()
    return jsonify({'success': 'OK'})



