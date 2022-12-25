from datetime import datetime
from flask import Flask, url_for, request, session, redirect
from flask import render_template
from bcrypt import hashpw, gensalt, checkpw
from re import compile, sub
from src.form import RegisterForm, LoginForm, ProjectForm, SprintForm, TaskForm, UserForm, UserStory
from src import db
from src.model.project import Project
from src.model.sprint import Sprint
from src.model.task import Task
from src.model.user import User
from src.model.story import Story
from src.model.login_attempt import LoginAttempt
from sqlalchemy import asc, desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
db.init_app(app)


@app.template_filter()
def strftime(value, fmt="%H:%M %d-%m-%y"):
    return value.strftime(fmt)


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return redirect(url_for('project'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if checkpw(request.form['password'].encode('utf-8'), the_user.password_hash):
            session['user'] = the_user.first_name
            session['user_id'] = the_user.user_id
            return redirect(url_for('project'))
        login_form.password.errors = ["Incorrect username or password."]
        new_login_attempt = LoginAttempt(email=request.form['email'], password=request.form['password'].encode('utf-8'))
        db.session.add(new_login_attempt)
        db.session.commit()
        return render_template("app/login.html", form=login_form)
    else:
        return render_template("app/login.html", form=login_form)




@app.route('/project', methods=['POST', 'GET'])
@app.route('/project/<project_id>', methods=['POST', 'GET'])
def project(project_id=None):
    sort_fn = lambda sprint: sprint.name
    next_sort = 'date'
    reverse = False
    if 'sort' in request.args and request.args.get('sort') == 'date':
        sort_fn = lambda sprint: sprint.created_at
        reverse = True
        next_sort = 'alpha'
    if 'sort' in request.args and request.args.get('sort') == 'alpha':
        sort_fn = lambda sprint: sprint.name
        reverse = False
        next_sort = 'date'

    user = db.session.query(User).filter_by(user_id=session.get('user_id')).one()
    active_project = None
    is_owner = False
    if project_id is not None:
        active_project = db.session.query(Project).filter_by(project_id=project_id).one()
        active_project.sprints.sort(key=sort_fn, reverse=reverse)
        is_owner = (active_project.created_by.user_id == user.user_id)
    elif len(user.projects) != 0:
        return redirect(url_for('project', project_id=user.projects[0].project_id))
    project_form = ProjectForm()
    sprint_form = SprintForm()
    task_form = TaskForm()
    return render_template("app/project.html", next_sort=next_sort,
                           project_form=project_form,
                           sprint_form=sprint_form,
                           task_form=task_form,
                           projects=user.projects, active_project=active_project, is_owner=is_owner)


@app.route('/project/add', methods=['POST', 'GET'])
def project_add():
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        user = db.session.query(User).filter_by(user_id=session.get('user_id')).one()
        new_project = Project(name=request.form['name'], created_by=user)
        new_project.users.append(user)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('project', project_id=new_project.project_id))
    return redirect(url_for('project'))


@app.route('/sprint/add/<project_id>', methods=['POST', 'GET'])
def sprint_add(project_id: int):
    sprint_form = SprintForm()
    if sprint_form.validate_on_submit():
        p: Project = db.session.query(Project).filter_by(project_id=project_id).one()
        sprint: Sprint = Sprint(name=request.form['name'], project=p)
        db.session.add(sprint)
        db.session.commit()
        return redirect(url_for('project', project_id=project_id))
    return redirect(url_for('project', project_id=project_id))


@app.route('/sprint/delete/<project_id>/<sprint_id>', methods=['POST', 'GET'])
def sprint_delete(project_id, sprint_id):
    sprint = db.session.query(Sprint).filter_by(sprint_id=sprint_id).one()
    if sprint is not None:
        db.session.delete(sprint)
        db.session.commit()
    return redirect(url_for('project', project_id=project_id))


@app.route('/task/add/<project_id>/<sprint_id>', methods=['POST', 'GET'])
def task_add(project_id, sprint_id):
    task_form = TaskForm()
    desc_filter = compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = sub(desc_filter, '', request.form['description'])

    if task_form.validate_on_submit():
        s = db.session.query(Sprint).filter_by(sprint_id=sprint_id).one()
        task = Task(name=request.form['name'], description=cleantext, sprint=s)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('project', project_id=project_id))
    return redirect(url_for('project', project_id=project_id))


@app.route('/task/delete/<project_id>/<task_id>', methods=['POST', 'GET'])
def task_delete(project_id, task_id):
    task = db.session.query(Task).filter_by(task_id=task_id).one()
    if task is not None:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('project', project_id=project_id))


@app.route('/story/<project_id>', methods=['POST', 'GET'])
def story(project_id):
    project_form = ProjectForm()
    user_story = UserStory()
    user = db.session.query(User).filter_by(user_id=session.get('user_id')).one()
    active_project = db.session.query(Project).filter_by(project_id=project_id).one()
    is_owner = (active_project.created_by.user_id is user.user_id)

    return render_template("app/story.html",
                           is_owner=is_owner,
                           project_form=project_form,
                           user_story=user_story,
                           active_project=active_project,
                           projects=user.projects)


@app.route('/story/add/<project_id>', methods=['POST', 'GET'])
def story_add(project_id):
    user_story = UserStory()
    active_project = db.session.query(Project).filter_by(project_id=project_id).one()

    if user_story.validate_on_submit():
        new_story = Story(content=request.form['content'])
        db.session.add(new_story)
        db.session.commit()
        active_project.stories.append(new_story)
        db.session.commit()
    return redirect(url_for('story', project_id=project_id))


@app.route('/story/delete/<project_id>/<story_id>', methods=['GET'])
def story_delete(project_id, story_id):
    s = db.session.query(Story).filter_by(story_id=story_id).one()
    p = db.session.query(Project).filter_by(project_id=project_id).one()
    p.stories.remove(s)
    db.session.commit()
    return redirect(url_for('story', project_id=project_id))


@app.route('/users/<project_id>', methods=['POST', 'GET'])
def users(project_id):
    project_form = ProjectForm()
    user_form = UserForm()
    user = db.session.query(User).filter_by(user_id=session.get('user_id')).one()
    active_project = db.session.query(Project).filter_by(project_id=project_id).one()
    is_owner = (active_project.created_by.user_id is user.user_id)
    if not is_owner:
        return redirect(url_for('project'))
    return render_template("app/users.html",
                           is_owner=is_owner,
                           project_form=project_form,
                           user_form=user_form,
                           active_project=active_project,
                           projects=user.projects)


@app.route('/users/add/<project_id>', methods=['GET', 'POST'])
def user_add(project_id):
    user_form = UserForm()
    p = db.session.query(Project).filter_by(project_id=project_id).one()
    if user_form.validate_on_submit():
        new_user = db.session.query(User).filter_by(email=request.form['email']).one()
        p.users.append(new_user)
        db.session.commit()
    return redirect(url_for('project', project_id=project_id))


@app.route('/users/delete/<project_id>/<user_id>', methods=['GET'])
def user_remove(project_id, user_id):
    p = db.session.query(Project).filter_by(project_id=project_id).one()
    u = db.session.query(User).filter_by(user_id=user_id).one()
    p.users.remove(u)
    db.session.commit()
    return redirect(url_for('project', project_id=project_id))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        h_password = hashpw(request.form['password'].encode('utf-8'), gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_user = User(first_name=first_name, last_name=last_name, email=request.form['email'],
                        password_hash=h_password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = first_name
        session['user_id'] = new_user.user_id
        return redirect(url_for('project'))
    return render_template('app/register.html', form=form)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
