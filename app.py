import json

from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)


def load_form(layer):
    try:
        with open("d3.json", 'r') as d3json:
            parsed = json.loads("d3.json".read())
            return parsed
    finally:
        return 0


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html',
                           x=500,
                           y=500,
                           layer1=load_form(1),
                           layer2=1,
                           layer3=1,
                           layer4=1,
                           layer5=1, )


@app.route("/d3json", methods=["GET"])
def d3json():
    return send_file('d3.json')


@app.route("/createjson", methods=["POST"])
def createjson():
    layer1nodes = request.form.get("layer1")
    layer2nodes = request.form.get("layer2")
    layer3nodes = request.form.get("layer3")
    layer4nodes = request.form.get("layer4")
    layer5nodes = request.form.get("layer5")
    layer1nodesint = int(layer1nodes)
    layer2nodesint = int(layer2nodes)
    layer3nodesint = int(layer3nodes)
    layer4nodesint = int(layer4nodes)
    layer5nodesint = int(layer5nodes)
    # if layer1nodesint < 1:
    #    pass
    json_file = "d3.json"
    # Create an empty new dict
    d = {'layer1': [layer1nodesint], 'layer2': [layer2nodesint], 'layer3': [layer3nodesint],
         'layer4': [layer4nodesint], 'layer5': [layer5nodesint]}
    try:
        with open(json_file, "w") as d3_json_out:
            json.dump(d, d3_json_out, indent=4, sort_keys=False)
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return "Failed to open network.json file. Are you sure it is named correctly?"
