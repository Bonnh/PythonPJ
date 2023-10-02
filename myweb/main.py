from flask import Flask, render_template, request
from forms import SignUpForm


app = Flask(__name__)
app.config['SECRET_KEY']="HideOnBonh"
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
    
    # code html trong python
    # return'''
    # <html>
    #     <head>
    #         <title>
    #         To do list app
    #         </title>
    #     </head>
    #     <body>
    #         <div>
    #             <h1>To do list app</h1>
    #             <p>
    #                 <a href="#">Sign up now<a>
    #             </p>
    #         </div>
    #         <div>
    #             <h4>''' + todolist[0]['name'] + '''</h4>
    #             <p>''' + todolist[0]['description'] + '''</p>
    #             <h4>''' + todolist[1]['name'] + '''</h4>
    #             <p>''' + todolist[1]['description'] + '''</p>
    #         </div>
    #     </body>
    # </html>'''
    
    #truy cập vào file index.html
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

        
        user = {'fname':_fname,'lname':_lname, 'email':_email, 'password':_password}
        return render_template('signUpSuccess.html',user = user)
    
    print("Not validate on submit")
    return render_template('signup.html', form = form)

if  __name__ == '__main__':
    # app.run()
    app.run(host='127.0.0.1', port='8080', debug=True)