from flask import *
from forms import *
from flask_sqlalchemy import *
from flask_migrate import *
import os

baseDir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HideOnBonh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
import models


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', is_logged_in=is_logged_in())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect('/userhome')

    form = LoginForm()
    error = None
    if form.validate_on_submit():
        # List of all data in request
        _email = form.email.data
        _password = form.password.data

        # Check exist email
        user = db.session.query(models.User).filter_by(email=_email).first()

        if user is None:
            flash(f'Email {_email} does not exist')
        else:
            # Check password
            if user.check_password(_password):
                session['user_id'] = user.user_id
                return render_template('userhome.html', user=user)
            else:
                flash(f'Password is incorrect')

        # return do_the_login(request)
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.get('/signup')
def signup_get():
    form = SignupForm()
    return render_template('signup.html', form=form)


@app.post('/signup')
def signup_post():
    form = SignupForm()
    print(form.data)
    if form.validate_on_submit():
        print('Form validated')
        _first_name = form.first_name.data
        _last_name = form.last_name.data
        _email = form.email.data
        _password = form.password.data

        if db.session.query(models.User).filter_by(email=_email).count() == 0:
            new_user = models.User(
                first_name=_first_name,
                last_name=_last_name,
                email=_email,
            )

            new_user.set_password(_password)
            db.session.add(new_user)
            db.session.commit()

            return render_template('sign-up-succeed.html', user=new_user)
        else:
            flash(f'Email {_email} already exists')
            return render_template('signup.html', form=form)

    print(form.errors)

    print('Form not validated')
    return render_template('signup.html', form=form)


def is_logged_in():
    return session.get('user_id') is not None


@app.route('/projects', methods=['GET', 'POST'])
def projects_list():
    if not is_logged_in():
        return redirect('/login')

    _user_id = session.get('user_id')

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        return render_template('projects.html', user=user, is_logged_in=is_logged_in())
    else:
        return redirect('/login')


@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    form = ProjectForm()

    form.status.choices = [
        (s.status_id, s.desc) for s in db.session.query(models.Status).all()
    ]

    if is_logged_in():
        user = db.session.query(models.User).filter_by(user_id=session.get('user_id')).first()

        if form.validate_on_submit():
            _name = form.name.data

            _description = form.desc.data

            _deadline = form.deadline.data

            _status_id = form.status.data
            _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

            _project_id = request.form['hiddenProjectId']

            if _project_id == '0':
                project = models.Project(
                    name=_name,
                    deadline=_deadline,
                    desc=_description, user=user, status=_status
                )
                db.session.add(project)

            db.session.commit()
            return redirect('/projects')
        else:
            return render_template('new-project.html', form=form, user=user)
    redirect('/')


@app.route('/delete_project', methods=['GET', 'POST'])
def delete_project():
    _user_id = session.get('user_id')
    if _user_id:
        _project_id = request.form['hiddenProjectId']
        if _project_id:
            project = db.session.query(models.Project).filter_by(project_id=_project_id).first()
            db.session.delete(project)
            db.session.commit()

        return redirect('/projects')

    return redirect('/login')


@app.route('/edit_project', methods=['GET', 'POST'])
def edit_project():
    form = ProjectForm()

    form.status.choices = [
        (s.status_id, s.desc) for s in db.session.query(models.Status).all()
    ]

    _user_id = session.get('user_id')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _project_id = request.form['hiddenProjectId']
        print("_project_id: " + _project_id)
        if _project_id:
            if form.submitUpdate.data:
                print('Update project', form.data)
                _name = form.name.data

                _description = form.desc.data

                _deadline = form.deadline.data

                _status_id = form.status.data
                _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

                project = db.session.query(models.Project).filter_by(project_id=_project_id).first()

                project.name = _name
                project.desc = _description
                project.deadline = _deadline
                project.status = _status

                db.session.commit()
                return redirect('/projects')
            else:
                project = db.session.query(models.Project).filter_by(project_id=_project_id).first()
                form.process()

                form.name.data = project.name
                form.desc.data = project.desc
                form.deadline.data = project.deadline
                form.status.data = project.status.status_id

                return render_template('new-project.html', form=form, user=user, project=project)
        elif form.validate_on_submit():
            print('Form validated')

    return redirect('/')


@app.route('/project_detail/<projectId>', methods=['GET'])
def project_detail(projectId):
    _user_id = session.get('user_id')
    if not _user_id:
        return redirect('/login')

    user = db.session.query(models.User).filter_by(user_id=_user_id).first()
    project = db.session.query(models.Project).filter_by(project_id=projectId).first()

    return render_template('project_detail.html', user=user, project=project)


@app.route('/userhome', methods=['GET', 'POST'])
def user_home():
    if not is_logged_in():
        return redirect('/login')

    _user_id = session.get('user_id')

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        return render_template('userhome.html', user=user, is_logged_in=is_logged_in())
    else:
        return redirect('/login')


@app.route('/newTask', methods=['GET', 'POST'])
def new_task():
    form = TaskForm()
    form.priority.choices = [
        (p.priority_id, p.desc) for p in db.session.query(models.Priority).all()
    ]

    if is_logged_in():
        user = db.session.query(models.User).filter_by(user_id=session.get('user_id')).first()

        if form.validate_on_submit():
            _description = form.description.data

            _priority_id = form.priority.data
            _priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

            _task_id = request.form['hiddenTaskId']
            print(_task_id)

            if _task_id == '0':
                task = models.Task(description=_description, user=user, priority=_priority)
                db.session.add(task)

            db.session.commit()
            return redirect('/userhome')
        else:
            return render_template('new-task.html', form=form, user=user)
    redirect('/')


@app.route('/new_task/<projectId>', methods=['GET', 'POST'])
def new_task_by_project(projectId):
    form = TaskForm()

    form.priority.choices = [
        (p.priority_id, p.desc) for p in db.session.query(models.Priority).all()
    ]

    form.status.choices = [
        (s.status_id, s.desc) for s in db.session.query(models.Status).all()
    ]

    if is_logged_in():
        user = db.session.query(models.User).filter_by(user_id=session.get('user_id')).first()

        project = db.session.query(models.Project).filter_by(project_id=projectId).first()

        if form.deadline.data:
            print('form Deadline', form.deadline.data, type(form.deadline.data))
            print('project Deadline', project.deadline, type(project.deadline))
            if form.deadline.data > project.deadline:
                print('Deadline is invalid')
                # flash(f'Deadline must be before {project.deadline}')
            else:
                print('Deadline is valid')

        if form.validate_on_submit():
            _description = form.description.data

            _priority_id = form.priority.data
            _priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

            _status_id = form.status.data
            _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

            _task_id = request.form['hiddenTaskId']

            _deadline = form.deadline.data

            if _task_id == '0':
                task = models.Task(
                    description=_description, project=project, priority=_priority, status=_status,
                    deadline=_deadline
                )
                db.session.add(task)

            db.session.commit()
            check_if_all_tasks_in_projects_completed(projectId)
            return redirect('/project_detail/' + projectId)
        else:
            return render_template('new-task.html', form=form, user=user, project=project)
    redirect('/')


@app.route('/deleteTask', methods=['GET', 'POST'])
def delete_task():
    _user_id = session.get('user_id')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            print("task: ", task)
            db.session.delete(task)
            db.session.commit()

        return redirect('/userhome')

    return redirect('/login')


@app.route('/delete_task/<projectId>', methods=['GET', 'POST'])
def delete_task_redirect_to_project(projectId):
    _user_id = session.get('user_id')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            db.session.delete(task)
            db.session.commit()

        return redirect('/project_detail/' + projectId)

    return redirect('/login')


@app.route('/editTask', methods=['GET', 'POST'])
def edit_task():
    form = TaskForm()
    form.priority.choices = [
        (p.priority_id, p.desc) for p in db.session.query(models.Priority).all()
    ]

    _user_id = session.get('user_id')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            if form.submitUpdate.data:
                print('Update task', form.data)
                _description = form.description.data
                _priority_id = form.priority.data
                _priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                task.description = _description
                task.priority = _priority
                db.session.commit()
                return redirect('/userhome')
            else:
                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                form.process()
                form.description.data = task.description
                form.priority.data = task.priority.priority_id
                return render_template('new-task.html', form=form, user=user, task=task)
        elif form.validate_on_submit():
            print('Form validated')

    return redirect('/')


@app.route('/edit_task/<projectId>', methods=['GET', 'POST'])
def edit_task_by_project(projectId):
    form = TaskForm()

    form.priority.choices = [
        (p.priority_id, p.desc) for p in db.session.query(models.Priority).all()
    ]

    form.status.choices = [
        (s.status_id, s.desc) for s in db.session.query(models.Status).all()
    ]

    _user_id = session.get('user_id')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _task_id = request.form['hiddenTaskId']
        project = db.session.query(models.Project).filter_by(project_id=projectId).first()
        if _task_id:
            if form.submitUpdate.data:
                print('Update task', form.data)
                _description = form.description.data

                _priority_id = form.priority.data
                _priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

                _status_id = form.status.data
                _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

                if _status.desc == 'Đang thực hiện':
                    update_project_status(projectId, _status_id)

                _deadline = form.deadline.data

                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                task.description = _description
                task.priority = _priority
                task.status = _status
                task.deadline = _deadline

                db.session.commit()
                check_if_all_tasks_in_projects_completed(projectId)
                return redirect('/project_detail/' + projectId)
            else:
                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                form.process()
                form.description.data = task.description
                form.priority.data = task.priority.priority_id
                form.status.data = task.status.status_id
                form.deadline.data = task.deadline
                check_if_all_tasks_in_projects_completed(projectId)
                return render_template('new-task.html', form=form, user=user, task=task)
        elif form.validate_on_submit():
            print('Form validated')

    return redirect('/')


@app.route('/doneTask', methods=['GET', 'POST'])
def done_task():
    _user_id = session.get('user_id')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            task.isCompleted = True
            db.session.commit()

        return redirect('/userhome')

    return redirect('/')


def update_project_status(project_id, status_id):
    project = db.session.query(models.Project).filter_by(project_id=project_id).first()
    project.status_id = status_id
    db.session.commit()


def check_if_all_tasks_in_projects_completed(project_id):
    tasks = db.session.query(models.Task).filter_by(project_id=project_id).all()
    count = 0
    for task in tasks:
        if task.status.desc == 'Hoàn thành':
            count += 1
    if count == len(tasks):
        update_project_status(project_id, 4)
    else:
        update_project_status(project_id, 2)


with app.test_request_context():
    print(url_for('static', filename='style.css'))

if __name__ == '__main__':
    app.run()
