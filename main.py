from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.jobs import Jobs
from jobs_api import blueprint
from users_api import ublueprint
from data import jobs_resources
from data import users_resources
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__, template_folder='templates')
api = Api(app)
api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resources.JobsResource, '/api/v2/jobs/<int:jobs_id>')
api.add_resource(users_resources.UserListResource, '/api/v2/user')
api.add_resource(users_resources.UserResource, '/api/v2/user/<int:user_id>')




app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    position = StringField('Позиция', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class AddjobForm(FlaskForm):
    is_finished = BooleanField('Is job finished?')
    job = StringField('Title', validators=[DataRequired()])
    team_leader = StringField('Team Leader', validators=[DataRequired()])
    work_size = StringField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    submit = SubmitField('Add job')


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/jobs')
def base():
    db_session.global_init("db/blogs.sqlite")
    session = db_session.create_session()
    return render_template('main.html', title='Main', items=session.query(Jobs).all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=int(form.age.data),
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = AddjobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.id == int(form.team_leader.data)).first():
            job = Jobs(
                team_leader=int(form.team_leader.data),
                is_finished=form.is_finished.data,
                job=form.job.data,
                work_size=int(form.work_size.data),
                collaborators=form.collaborators.data
            )
            current_user.jobs.append(job)
            session.merge(current_user)
            session.commit()
            return redirect('/')
        return render_template('addjob.html', title='Adding a job', form=form, message="Такого пользователя нет")
    return render_template('addjob.html', title='Adding a job', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = AddjobForm()
    if request.method == "GET":
        session = db_session.create_session()
        if current_user.id == 1:
            jobs = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            jobs = session.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if jobs:
            form.team_leader.data = str(jobs.team_leader),
            print([str(jobs.team_leader), str(jobs.work_size), jobs.collaborators])
            form.is_finished.data = jobs.is_finished,
            form.job.data = jobs.job,
            form.work_size.data = jobs.collaborators,
            form.collaborators.data = jobs.work_size
        else:
            abort(404)

    if form.validate_on_submit():
        session = db_session.create_session()
        if current_user.id == 1:
            jobs = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            jobs = session.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if jobs:
            jobs.team_leader = int(form.team_leader.data),
            jobs.is_finished = form.is_finished.data,
            jobs.job = form.job.data,
            jobs.work_size = int(form.work_size.data),
            jobs.collaborators = form.collaborators.data
            session.commit()
            return redirect('/')
        else:
            abort(404)

    return render_template('addjob.html', title='Job changing', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    session = db_session.create_session()
    if current_user.id == 1:
        jobs = session.query(Jobs).filter(Jobs.id == id).first()
    else:
        jobs = session.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
    if jobs:
        session.delete(jobs)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(blueprint)
    app.register_blueprint(ublueprint)
    app.run()


if __name__ == '__main__':
    main()
