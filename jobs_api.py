from flask import Blueprint, request, jsonify
from requests import get
from data import db_session
from data.jobs import Jobs

blueprint = Blueprint('jobs_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'job', 'is_finished', 'work_size', 'collaborators')) for item in jobs]
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'work_size', 'team_leader', 'is_finished', 'collaborators', 'id']):
        return jsonify({'error': 'Bad request'})
    elif str(get(f'http://localhost:5000/api/jobs/{request.json["id"]}').json()) != '''{'error': 'Not found'}''':
        return jsonify({'error': 'Id already exists'})
    session = db_session.create_session()
    jobs = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        team_leader=request.json['team_leader'],
        is_finished=request.json['is_finished'],
        collaborators=request.json['collaborators']
    )
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id', 'job', 'is_finished', 'work_size', 'collaborators'))
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['POST'])
def change_jobs(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif str(get(f'http://localhost:5000/api/jobs/{jobs_id}').json()) == '''{'error': 'Not found'}''':
        return jsonify({'error': 'Id doesn\'t exist'})
    elif not any(key in request.json for key in
                 ['job', 'work_size', 'team_leader', 'is_finished', 'collaborators']):
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if 'team_leader' in request.json:
        jobs.team_leader = request.json['team_leader']
    if 'is_finished' in request.json:
        jobs.is_finished = request.json['is_finished']
    if 'job' in request.json:
        jobs.job = request.json['job']
    if 'work_size' in request.json:
        jobs.work_size = request.json['work_size']
    if 'collaborators' in request.json:
        jobs.collaborators = request.json['collaborators']
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    session.delete(jobs)
    session.commit()
    return jsonify({'success': 'OK'})
