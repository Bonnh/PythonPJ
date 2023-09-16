from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')

# def main():
#     return '"Hello"'
# if  __name__ == '__main__':
#     # app.run()
#     app.run(host='127.0.0.1', port='8080', debug=True)

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

if  __name__ == '__main__':
    # app.run()
    app.run(host='127.0.0.1', port='8080', debug=True)