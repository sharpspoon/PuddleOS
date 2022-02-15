import json

from flask import Flask, render_template, request, redirect, url_for, send_file


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    db = open("d3.json")
    data = json.load(db)
    try:
        return render_template('index.html',
                               x=data['x'],
                               y=data['y'],
                               layer1=data['layer1'],
                               layer2=data['layer2'],
                               layer3=data['layer3'],
                               layer4=data['layer4'],
                               layer5=data['layer5'], )
    except Exception as e:
        print(e)
        return render_template('index.html')


@app.route("/d3json", methods=["GET"])
def d3json():
    return send_file('d3.json')


@app.route("/graphjs", methods=["GET"])
def graphjs():
    return send_file('graph.js')


@app.route("/createjson", methods=["POST"])
def createjson():
    layer1nodes = request.form.get("layer1")
    layer2nodes = request.form.get("layer2")
    layer3nodes = request.form.get("layer3")
    layer4nodes = request.form.get("layer4")
    layer5nodes = request.form.get("layer5")
    x = request.form.get("x")
    y = request.form.get("y")
    layer1nodesint = int(layer1nodes)
    layer2nodesint = int(layer2nodes)
    layer3nodesint = int(layer3nodes)
    layer4nodesint = int(layer4nodes)
    layer5nodesint = int(layer5nodes)
    xint = int(x)
    yint = int(y)

    json_file = "d3.json"
    d = {'x': xint, 'y': yint, 'layer1': layer1nodesint, 'layer2': layer2nodesint, 'layer3': layer3nodesint,
         'layer4': layer4nodesint, 'layer5': layer5nodesint}
    try:
        with open(json_file, "w") as d3_json_out:
            json.dump(d, d3_json_out, indent=4, sort_keys=False)
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return "Failed to open d3.json file."
