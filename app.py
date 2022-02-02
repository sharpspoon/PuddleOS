from flask import Flask, render_template

app = Flask(__name__)

print('''
.-,--.       .   . .      ,,--. .---. 
 '|__/ . . ,-| ,-| |  ,-. |`, | \___  
 ,|    | | | | | | |  |-' |   |     \ 
 `'    `-^ `-^ `-^ `' `-' `---' `---' 
 ''')


@app.route("/")
def hello_world():
    return render_template('index.html',
                           title='Home Page')
