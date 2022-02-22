import json
import random

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
                               layer1=data['layer1total'],
                               layer1color=data['layer1color'],
                               layer2=data['layer2total'],
                               layer2color=data['layer2color'],
                               layer3=data['layer3total'],
                               layer3color=data['layer3color'],
                               layer4=data['layer4total'],
                               layer4color=data['layer4color'],
                               layer5=data['layer5total'],
                               layer5color=data['layer5color'])
    except Exception as e:
        print(e)
        return render_template('index.html')


@app.route("/d3json", methods=["GET"])
def d3json():
    return send_file('d3.json')


@app.route("/d3js", methods=["GET"])
def graphjs():
    return send_file('d3.js')


@app.route("/createjson", methods=["POST"])
def createjson():
    layer1nodes = request.form.get("layer1")
    layer2nodes = request.form.get("layer2")
    layer3nodes = request.form.get("layer3")
    layer4nodes = request.form.get("layer4")
    layer5nodes = request.form.get("layer5")

    layer1color = request.form.get("colorInput1")
    layer2color = request.form.get("colorInput2")
    layer3color = request.form.get("colorInput3")
    layer4color = request.form.get("colorInput4")
    layer5color = request.form.get("colorInput5")

    x = request.form.get("x")
    y = request.form.get("y")

    layer1nodesint = int(layer1nodes)
    layer2nodesint = int(layer2nodes)
    layer3nodesint = int(layer3nodes)
    layer4nodesint = int(layer4nodes)
    layer5nodesint = int(layer5nodes)
    xint = int(x)
    yint = int(y)

    d = {'x': xint,
         'y': yint,
         'layer1total': layer1nodesint,
         'layer1color': layer1color,
         'layer2total': layer2nodesint,
         'layer2color': layer2color,
         'layer3total': layer3nodesint,
         'layer3color': layer3color,
         'layer4total': layer4nodesint,
         'layer4color': layer4color,
         'layer5total': layer5nodesint,
         'layer5color': layer5color,
         'nodes': [],
         'links': []}

    for i in range(layer1nodesint):
        d['nodes'].append({'id': i, 'group': 1, 'size': 4, 'fixed': True,
                           'x': random.randrange(0, xint), 'y': random.randrange(0, yint)})
    for i in range(layer2nodesint):
        d['nodes'].append({'id': i, 'group': 2, 'size': 8, 'fixed': True,
                           'x': random.randrange(0, xint), 'y': random.randrange(0, yint)})
    for i in range(layer3nodesint):
        d['nodes'].append({'id': i, 'group': 3, 'size': 10, 'fixed': True,
                           'x': random.randrange(0, xint), 'y': random.randrange(0, yint)})
    for i in range(layer4nodesint):
        d['nodes'].append({'id': i, 'group': 4, 'size': 12, 'fixed': True,
                           'x': random.randrange(0, xint), 'y': random.randrange(0, yint)})
    for i in range(layer5nodesint):
        d['nodes'].append({'id': i, 'group': 5, 'size': 20, 'fixed': True,
                           'x': random.randrange(0, xint), 'y': random.randrange(0, yint)})

    json_file = "d3.json"

    try:
        with open(json_file, "w") as d3_json_out:
            json.dump(d, d3_json_out, indent=4, sort_keys=False)
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return "Failed to open d3.json file."
