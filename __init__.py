from flask import Flask, render_template, request

import main

app = Flask(__name__)

print('''
.-,--.       .   . .      ,,--. .---. 
 '|__/ . . ,-| ,-| |  ,-. |`, | \___  
 ,|    | | | | | | |  |-' |   |     \ 
 `'    `-^ `-^ `-^ `' `-' `---' `---' 
 ''')


@app.route("/")
def _index():
    return render_template('index.html',
                           title='Home Page')


@app.route("/createjson", methods=["POST"])
def _createjson():
    layer1nodes = request.form.get("layer1")
    return main.createjson(layer1nodes)
