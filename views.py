import main
from flask import render_template, request

@app.route("/")
def _index():
    return render_template('index.html',
                           title='Home Page')


@app.route("/createjson", methods=["POST"])
def _createjson():
    layer1nodes = request.form.get("layer1")
    layer1nodesint = int(layer1nodes)
    if layer1nodesint < 1:
        pass
    return main.createjson(layer1nodes)
