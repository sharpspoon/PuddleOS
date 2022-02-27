import json
import random

from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    db = open("d3.json")
    data = json.load(db)

    if data['layer1visible'] == "on":
        layer1display = "checked"
    else:
        layer1display = ""

    if data['layer2visible'] == "on":
        layer2display = "checked"
    else:
        layer2display = ""

    if data['layer3visible'] == "on":
        layer3display = "checked"
    else:
        layer3display = ""

    if data['layer4visible'] == "on":
        layer4display = "checked"
    else:
        layer4display = ""

    if data['layer5visible'] == "on":
        layer5display = "checked"
    else:
        layer5display = ""
    try:
        return render_template('index.html',
                               x=data['x'],
                               y=data['y'],
                               z=data['z'],

                               layer1=data['layer1total'],
                               layer1color=data['layer1color'],
                               layer1visible=layer1display,

                               layer2=data['layer2total'],
                               layer2color=data['layer2color'],
                               layer2visible=layer2display,

                               layer3=data['layer3total'],
                               layer3color=data['layer3color'],
                               layer3visible=layer3display,

                               layer4=data['layer4total'],
                               layer4color=data['layer4color'],
                               layer4visible=layer4display,

                               layer5=data['layer5total'],
                               layer5color=data['layer5color'],
                               layer5visible=layer5display,)
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

    layer1visibled3 = request.form.get("nodeDisplay1")
    layer2visibled3 = request.form.get("nodeDisplay2")
    layer3visibled3 = request.form.get("nodeDisplay3")
    layer4visibled3 = request.form.get("nodeDisplay4")
    layer5visibled3 = request.form.get("nodeDisplay5")

    if layer1visibled3 == "on":
        layer1visible = "visible"
    else:
        layer1visible = "hidden"

    if layer2visibled3 == "on":
        layer2visible = "visible"
    else:
        layer2visible = "hidden"

    if layer3visibled3 == "on":
        layer3visible = "visible"
    else:
        layer3visible = "hidden"

    if layer4visibled3 == "on":
        layer4visible = "visible"
    else:
        layer4visible = "hidden"

    if layer5visibled3 == "on":
        layer5visible = "visible"
    else:
        layer5visible = "hidden"

    x = request.form.get("x")
    y = request.form.get("y")
    z = request.form.get("z")

    layer1nodesint = int(layer1nodes)
    layer2nodesint = int(layer2nodes)
    layer3nodesint = int(layer3nodes)
    layer4nodesint = int(layer4nodes)
    layer5nodesint = int(layer5nodes)

    xint = int(x)
    yint = int(y)
    zint = int(z)

    d = {'x': xint,
         'y': yint,
         'z': zint,
         'layer1total': layer1nodesint,
         'layer1color': layer1color,
         'layer1visible': layer1visibled3,
         'layer2total': layer2nodesint,
         'layer2color': layer2color,
         'layer2visible': layer2visibled3,
         'layer3total': layer3nodesint,
         'layer3color': layer3color,
         'layer3visible': layer3visibled3,
         'layer4total': layer4nodesint,
         'layer4color': layer4color,
         'layer4visible': layer4visibled3,
         'layer5total': layer5nodesint,
         'layer5color': layer5color,
         'layer5visible': layer5visibled3,
         'nodes': [],
         'links': []}

    for i in range(layer1nodesint):
        d['nodes'].append({'id': i, 'group': 1, 'size': 4, 'fixed': True,
                           'x': random.randrange(0, xint),
                           'y': random.randrange(0, yint),
                           'z': random.randrange(0, zint),
                           'color': layer1color,
                           'visibility': layer1visible})
    for i in range(layer2nodesint):
        d['nodes'].append({'id': i, 'group': 2, 'size': 8, 'fixed': True,
                           'x': random.randrange(0, xint),
                           'y': random.randrange(0, yint),
                           'z': random.randrange(0, zint),
                           'color': layer2color,
                           'visibility': layer2visible})
    for i in range(layer3nodesint):
        d['nodes'].append({'id': i, 'group': 3, 'size': 10, 'fixed': True,
                           'x': random.randrange(0, xint),
                           'y': random.randrange(0, yint),
                           'z': random.randrange(0, zint),
                           'color': layer3color,
                           'visibility': layer3visible})
    for i in range(layer4nodesint):
        d['nodes'].append({'id': i, 'group': 4, 'size': 12, 'fixed': True,
                           'x': random.randrange(0, xint),
                           'y': random.randrange(0, yint),
                           'z': random.randrange(0, zint),
                           'color': layer4color,
                           'visibility': layer4visible})
    for i in range(layer5nodesint):
        d['nodes'].append({'id': i, 'group': 5, 'size': 20, 'fixed': True,
                           'x': random.randrange(0, xint),
                           'y': random.randrange(0, yint),
                           'z': random.randrange(0, zint),
                           'color': layer5color,
                           'visibility': layer5visible})

    json_file = "d3.json"

    try:
        with open(json_file, "w") as d3_json_out:
            json.dump(d, d3_json_out, indent=4, sort_keys=False)
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return "Failed to open d3.json file."
