from flask import Blueprint, request, jsonify
from requests import get
from data import db_session
from data.users import User

ublueprint = Blueprint('user_api', __name__,
                      template_folder='templates')


@ublueprint.route('/api/user', methods=['GET'])
def get_user():
    session = db_session.create_session()
    user = session.query(User).all()
    return jsonify(
        {
            'user':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'email', 'position', 'speciality')) for item in
                 user]
        }
    )


@ublueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'work_size', 'team_leader', 'is_finished', 'collaborators', 'id']):
        return jsonify({'error': 'Bad request'})
    elif str(get(f'http://localhost:5000/api/user/{request.json["id"]}').json()) != '''{'error': 'Not found'}''':
        return jsonify({'error': 'Id already exists'})
    session = db_session.create_session()
    user = User(
        id=request.json['id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        team_leader=request.json['team_leader'],
        is_finished=request.json['is_finished'],
        collaborators=request.json['collaborators']
    )
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@ublueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'email', 'position', 'speciality'))
        }
    )


@ublueprint.route('/api/user/<int:user_id>', methods=['POST'])
def change_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif str(get(f'http://localhost:5000/api/user/{user_id}').json()) == '''{'error': 'Not found'}''':
        return jsonify({'error': 'Id doesn\'t exist'})
    elif not any(key in request.json for key in
                 ['surname', 'name', 'age', 'email', 'position', 'speciality']):
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if 'name' in request.json:
        user.name = request.json['name']
    if 'surname' in request.json:
        user.surname = request.json['surname']
    if 'position' in request.json:
        user.position = request.json['position']
    if 'speciality' in request.json:
        user.speciality = request.json['speciality']
    if 'age' in request.json:
        user.age = request.json['age']
    if 'email' in request.json:
        user.age = request.json['email']
    session.commit()
    return jsonify({'success': 'OK'})


@ublueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})
