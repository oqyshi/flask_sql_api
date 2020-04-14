from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.jobs import Jobs
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('collaborators', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('team_leader', required=True, type=int)


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"Jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(only=('job', 'work_size', 'user.name'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('job', 'work_size', 'user.name')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            is_finished=args['is_finished'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators']
        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})
