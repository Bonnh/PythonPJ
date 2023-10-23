import email
from flask import Flask, flash, session, redirect, render_template, request
from forms import SignInForm, SignUpForm, TaskForm
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
basedir = os.path.abspath(os.path.dirname(__file__))







app = Flask(__name__)
app.config['SECRET_KEY']="HideOnBonh"
app.config[ 'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy (app)
migrate = Migrate (app, db)
import models
#


# def main():
#     return '"Hello"'
# if  __name__ == '__main__':
#     # app.run()
#     app.run(host='127.0.0.1', port='8080', debug=True)

@app.route('/')
def main():
    todolist = [
        {
            'name':'Mua sữa',
            'description': 'Mua 2 lít sữa ở siêu thị Coopmart'
        },
        {
            'name':'Rút tiền',
            'description': 'Rút 500.000 vnđ từ cây TMA'
        }
    ]
    return render_template('index.html', todolist = todolist)

@app.route('/signup', methods=['GET','POST'])
def showsignup():
    form = SignUpForm()
    if form.validate_on_submit():
        print("Validate on submit")
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        if db.session.query(models.User).filter_by(email=_email).count() == 0:
            new_user = models.User(first_name = _fname, last_name = _lname, email=_email)
            new_user.set_password(_password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('signUpSuccess.html', user=new_user)
        else:
            flash(f'Email {_email} already exists')
            return render_template('signup.html', form=form)


    
    print("Not validate on submit")
    return render_template('signup.html', form = form)

@app.route('/signin', methods=['GET','POST'])
def signin():
    
    form = SignInForm()
    
    if form.validate_on_submit(): 
        _email = form.inputEmail.data 
        _password = form.inputPassword.data
    
        user = db.session.query(models.User).filter_by(email=_email).first() 
        if (user is None): 
            flash('Wrong email address or password!')
        else:
            if (user.check_password(_password)): 
                session['user'] = user.user_id 
                #return render_template('userhome.html') 
                return redirect('/userhome')
            else:
                flash('Wrong email address or password!')
    else:
        return render_template('signin.html',form = form)
    
@app.route('/userhome', methods=['GET', 'POST'])
def userHome():
    
    _user_id = session.get('user')
    
    if _user_id:
        user = db.session.query(models.User). filter_by(user_id=_user_id).first()
        return render_template('userhome.html', user = user)
    else:
        return redirect('/')

@app.route('/newTask', methods=['GET', 'POST'])
def newTask():
    _user_id = session.get('user')
    form = TaskForm()
    if _user_id:
        user = db.session.query(models. User). filter_by(user_id=_user_id).first()
        if form.validate_on_submit(): 
            _description = form. inputDescription.data 
            task = models.Task(description = _description, user = user) 
            db.session.add(task) 
            db.session.commit() 
            return redirect('/userhome')
        return render_template('/newtask.html', form = form, user = user)
    return redirect('/')


if  __name__ == '__main__':
    # app.run()
    app.run(host='127.0.0.1', port='8080', debug=True)