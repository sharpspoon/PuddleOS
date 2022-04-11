import json
import math
import random
from datetime import date
from uuid import uuid4
from flask import Flask, render_template, request, redirect, url_for, send_file, session
import database


# to make flask auto reload when python files are updated:
# $ export FLASK_ENV=development
# Do not use this in production
app = Flask(__name__)
# make flask reload when templates are updated
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = b'SecretKeyForSession'

# route anything starting with /database to database.py
app.register_blueprint(database.bp)

nodecountchange = False


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    data = None
    if 'uuid' in session:
        data = database.get_user_data(session['uuid'])
    else:
        try:
            with open("d3.json") as f:
                data = json.load(f)
        except FileNotFoundError:  
            print("Data json not found, exiting...")
            exit(1)
        session['uuid'] = uuid4()

    totalnodes = data['layer1total'] + data['layer2total'] + data['layer3total'] + data['layer4total'] + data[
        'layer5total']

    layer1display = "checked" if data['layer1visible'] == "on" else ""
    layer2display = "checked" if data['layer2visible'] == "on" else ""
    layer3display = "checked" if data['layer3visible'] == "on" else ""
    layer4display = "checked" if data['layer4visible'] == "on" else ""
    layer5display = "checked" if data['layer5visible'] == "on" else ""

    layer1puddledisplay = "checked" if data['layer1puddlevisible'] == "on" else ""
    layer2puddledisplay = "checked" if data['layer2puddlevisible'] == "on" else ""
    layer3puddledisplay = "checked" if data['layer3puddlevisible'] == "on" else ""
    layer4puddledisplay = "checked" if data['layer4puddlevisible'] == "on" else ""
    layer5puddledisplay = "checked" if data['layer5puddlevisible'] == "on" else ""

    layer1clutering = buildclusteringhtml(data['layer1clustering'])
    layer2clutering = buildclusteringhtml(data['layer2clustering'])
    layer3clutering = buildclusteringhtml(data['layer3clustering'])
    layer4clutering = buildclusteringhtml(data['layer4clustering'])
    layer5clutering = buildclusteringhtml(data['layer5clustering'])
    try:
        return render_template('index.html',
                               nodedata=data['nodes'],
                               year=date.today().year,
                               x=data['x'],
                               y=data['y'],
                               z=data['z'],
                               layer1=data['layer1total'],
                               layer1cluteringmethod=layer1clutering,
                               layer1color=data['layer1color'],
                               layer1visible=layer1display,
                               layer1size=data['layer1size'],
                               layer1puddlevisible=layer1puddledisplay,
                               layer2=data['layer2total'],
                               layer2cluteringmethod=layer2clutering,
                               layer2color=data['layer2color'],
                               layer2visible=layer2display,
                               layer2size=data['layer2size'],
                               layer2puddlevisible=layer2puddledisplay,
                               layer3=data['layer3total'],
                               layer3cluteringmethod=layer3clutering,
                               layer3color=data['layer3color'],
                               layer3visible=layer3display,
                               layer3size=data['layer3size'],
                               layer3puddlevisible=layer3puddledisplay,
                               layer4=data['layer4total'],
                               layer4cluteringmethod=layer4clutering,
                               layer4color=data['layer4color'],
                               layer4visible=layer4display,
                               layer4size=data['layer4size'],
                               layer4puddlevisible=layer4puddledisplay,
                               layer5=data['layer5total'],
                               layer5cluteringmethod=layer5clutering,
                               layer5color=data['layer5color'],
                               layer5visible=layer5display,
                               layer5size=data['layer5size'],
                               layer5puddlevisible=layer5puddledisplay,
                               totalnodes=totalnodes)
    except Exception as e:
        print(e)
        return render_template('index.html')

@app.route("/log", methods=["GET"])
def log():
    data = None
    try:
        with open("d3.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Data json not found, exiting...")
        exit(1)
    return render_template('log.html',
                           year=date.today().year,
                           log=data['log'])


@app.route("/nodedata", methods=["GET"])
def nodedata():
    data = None
    try:
        with open("d3.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Data json not found, exiting...")
        exit(1)
    return render_template('nodedata.html',
                           year=date.today().year,
                           nodedata=data['nodes'])


@app.route("/linkdata", methods=["GET"])
def linkdata():
    data = None
    try:
        with open("d3.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Data json not found, exiting...")
        exit(1)
    return render_template('linkdata.html',
                           year=date.today().year,
                           linkdata=data['links'])


@app.route("/d3json", methods=["GET"])
def d3json():
    return send_file('d3.json')


@app.route("/d3js", methods=["GET"])
def graphjs():
    return send_file('d3.js')


def buildclusteringhtml(method):
    ret = ""
    if method == "Agglomerative Complete Linkage Hierarchical Clustering":
        ret = '''<option value="Agglomerative Complete Linkage Hierarchical Clustering" selected>Agglomerative Complete Linkage Hierarchical Clustering</option>
        <option value="K-Means">K-Means</option>'''
    elif method == "K-Means":
        ret = '''<option value="Agglomerative Complete Linkage Hierarchical Clustering">Agglomerative Complete Linkage Hierarchical Clustering</option>
        <option value="K-Means" selected>K-Means</option>'''
    return ret


@app.route("/createjson", methods=["POST"])
def createjson():
    # Get all form values on submission.
    global nodecountchange
    nodecountchange = False
    layer1nodes = int(request.form.get("layer1"))
    layer2nodes = int(request.form.get("layer2"))
    layer3nodes = int(request.form.get("layer3"))
    layer4nodes = int(request.form.get("layer4"))
    layer5nodes = int(request.form.get("layer5"))
    layer1color = request.form.get("colorInput1")
    layer2color = request.form.get("colorInput2")
    layer3color = request.form.get("colorInput3")
    layer4color = request.form.get("colorInput4")
    layer5color = request.form.get("colorInput5")
    layer1size = int(request.form.get("layer1size"))
    layer2size = int(request.form.get("layer2size"))
    layer3size = int(request.form.get("layer3size"))
    layer4size = int(request.form.get("layer4size"))
    layer5size = int(request.form.get("layer5size"))
    layer1visibled3 = request.form.get("nodeDisplay1")
    layer2visibled3 = request.form.get("nodeDisplay2")
    layer3visibled3 = request.form.get("nodeDisplay3")
    layer4visibled3 = request.form.get("nodeDisplay4")
    layer5visibled3 = request.form.get("nodeDisplay5")
    layer1clustering = request.form.get("layer1ClusteringMethod")
    layer2clustering = request.form.get("layer2ClusteringMethod")
    layer3clustering = request.form.get("layer3ClusteringMethod")
    layer4clustering = request.form.get("layer4ClusteringMethod")
    layer5clustering = request.form.get("layer5ClusteringMethod")
    layer1puddlevisible = request.form.get("puddleDisplay1")
    layer2puddlevisible = request.form.get("puddleDisplay2")
    layer3puddlevisible = request.form.get("puddleDisplay3")
    layer4puddlevisible = request.form.get("puddleDisplay4")
    layer5puddlevisible = request.form.get("puddleDisplay5")
    randomizelayer1 = request.form.get("randomizeLayer1")
    randomizelayer2 = request.form.get("randomizeLayer2")
    randomizelayer3 = request.form.get("randomizeLayer3")
    randomizelayer4 = request.form.get("randomizeLayer4")
    randomizelayer5 = request.form.get("randomizeLayer5")
    x = request.form.get("x")
    y = request.form.get("y")
    z = request.form.get("z")

    # This logic is for setting the individual nodes to visible or hidden
    layer1visible = "visible" if layer1visibled3 == "on" else "hidden"
    layer2visible = "visible" if layer2visibled3 == "on" else "hidden"
    layer3visible = "visible" if layer3visibled3 == "on" else "hidden"
    layer4visible = "visible" if layer4visibled3 == "on" else "hidden"
    layer5visible = "visible" if layer5visibled3 == "on" else "hidden"

    totalnodes = layer1nodes + layer2nodes + layer3nodes + layer4nodes + layer5nodes
    layer1startid = 0
    layer2startid = layer1startid + layer1nodes
    layer3startid = layer2startid + layer2nodes
    layer4startid = layer3startid + layer3nodes
    layer5startid = layer4startid + layer4nodes
    xint = int(x)
    yint = int(y)
    zint = int(z)
    log = ""

    d = {'x': xint,
         'y': yint,
         'z': zint,
         'layer1total': layer1nodes,
         'layer1color': layer1color,
         'layer1size': layer1size,
         'layer1visible': layer1visibled3,
         'layer1clustering': layer1clustering,
         'layer1puddlevisible': layer1puddlevisible,
         'layer2total': layer2nodes,
         'layer2color': layer2color,
         'layer2size': layer2size,
         'layer2visible': layer2visibled3,
         'layer2clustering': layer2clustering,
         'layer2puddlevisible': layer2puddlevisible,
         'layer3total': layer3nodes,
         'layer3color': layer3color,
         'layer3size': layer3size,
         'layer3visible': layer3visibled3,
         'layer3clustering': layer3clustering,
         'layer3puddlevisible': layer3puddlevisible,
         'layer4total': layer4nodes,
         'layer4color': layer4color,
         'layer4size': layer4size,
         'layer4visible': layer4visibled3,
         'layer4clustering': layer4clustering,
         'layer4puddlevisible': layer4puddlevisible,
         'layer5total': layer5nodes,
         'layer5color': layer5color,
         'layer5size': layer5size,
         'layer5visible': layer5visibled3,
         'layer5clustering': layer5clustering,
         'layer5puddlevisible': layer5puddlevisible,
         'nodes': [],
         'links': [],
         'log': log}

    data = None
    try:
        with open("d3.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Data json not found, exiting...")
        exit(1)
    if layer1nodes != data['layer1total'] \
            or layer2nodes != data['layer2total'] \
            or layer3nodes != data['layer3total'] \
            or layer4nodes != data['layer4total'] \
            or layer5nodes != data['layer5total']:
        nodecountchange = True
    print(nodecountchange)

    # This function will create a new node with the specified parameters
    # If you need a different fx,fy,fz, you can specify it when called.
    def newNode(id, group, size, color, visibility,
                fx=None,
                fy=None,
                z=None):
        return {'id': id,
                'group': group,
                'size': size,
                'fixed': True,
                'fx': fx if fx else random.randrange(0, xint),
                'fy': fy if fy else random.randrange(0, yint),
                'z': z if z else random.randrange(0, zint),
                'color': color,
                'visibility': visibility}

    g = -1
    for i in range(layer1nodes):
        g += 1
        if nodecountchange is True or randomizelayer1 == "on":
            d['nodes'].append(newNode(g, 1, layer1size, layer1color, layer1visible))
        else:
            x = data['nodes'][layer1startid + i]['fx']
            y = data['nodes'][layer1startid + i]['fy']
            z = data['nodes'][layer1startid + i]['z']
            nodex = int(x)
            nodey = int(y)
            nodez = int(z)
            d['nodes'].append(newNode(g, 1, layer1size, layer1color, layer1visible, nodex, nodey, nodez))

    for i in range(layer2nodes):
        g += 1
        if nodecountchange is True or randomizelayer2 == "on":
            d['nodes'].append(newNode(g, 2, layer2size, layer2color, layer2visible))
        else:
            x = data['nodes'][layer2startid + i]['fx']
            y = data['nodes'][layer2startid + i]['fy']
            z = data['nodes'][layer2startid + i]['z']
            nodex = int(x)
            nodey = int(y)
            nodez = int(z)
            d['nodes'].append(newNode(g, 2, layer2size, layer2color, layer2visible, nodex, nodey, nodez))

    for i in range(layer3nodes):
        g += 1
        if nodecountchange is True or randomizelayer3 == "on":
            d['nodes'].append(newNode(g, 3, layer3size, layer3color, layer3visible))
        else:
            x = data['nodes'][layer3startid + i]['fx']
            y = data['nodes'][layer3startid + i]['fy']
            z = data['nodes'][layer3startid + i]['z']
            nodex = int(x)
            nodey = int(y)
            nodez = int(z)
            d['nodes'].append(newNode(g, 3, layer3size, layer3color, layer3visible, nodex, nodey, nodez))

    for i in range(layer4nodes):
        g += 1
        if nodecountchange is True or randomizelayer4 == "on":
            d['nodes'].append(newNode(g, 4, layer4size, layer4color, layer4visible))
        else:
            print(layer4startid)
            x = data['nodes'][layer4startid + i]['fx']
            y = data['nodes'][layer4startid + i]['fy']
            z = data['nodes'][layer4startid + i]['z']
            nodex = int(x)
            nodey = int(y)
            nodez = int(z)
            d['nodes'].append(newNode(g, 4, layer4size, layer4color, layer4visible, nodex, nodey, nodez))

    for i in range(layer5nodes):
        g += 1
        if nodecountchange is True or randomizelayer5 == "on":
            d['nodes'].append(newNode(g, 5, layer5size, layer5color, layer5visible))
        else:
            x = data['nodes'][layer5startid + i]['fx']
            y = data['nodes'][layer5startid + i]['fy']
            z = data['nodes'][layer5startid + i]['z']
            nodex = int(x)
            nodey = int(y)
            nodez = int(z)
            d['nodes'].append(newNode(g, 5, layer5size, layer5color, layer5visible, nodex, nodey, nodez))

    pid = 0  # Set the PuddleId to 0
    if layer1puddlevisible == "on":
        d['links'].append({'puddleid': 1, 'source': 1, 'target': 6})  # Placeholder, delete later

    if layer2puddlevisible == "on":
        for i in range(layer2startid, layer2startid + layer2nodes):
            # Get the node at the current index
            node_a = d['nodes'][i]
            if node_a['group'] == 2:  # If the current node is in group 2.
                pid += 1  # Increase the Puddle ID by 1 each time.

                # Set the previous, source, and destination x, y, z variables
                if d['nodes'][i - 1]['group'] == 2:  # If this previous node is in the same group
                    px = d['nodes'][i - 1]['fx']
                    py = d['nodes'][i - 1]['fy']
                    pz = d['nodes'][i - 1]['z']
                else:  # There is no previous node in this group.
                    px = None
                    py = None
                    pz = None

                xa = node_a['fx']
                ya = node_a['fy']
                za = node_a['z']

                identifier = d['nodes'][i]['id']
                bestdst = float('inf')
                bestdstid = None

                # For this current node, loop through all other nodes and find closest
                for j in range(layer2startid, layer2startid + layer2nodes):
                    # Set the current destination node location
                    node_b = d['nodes'][j]
                    xb = node_b['fx']
                    yb = node_b['fy']
                    zb = node_b['z']
                    idb = node_b['id']

                    # Only proceed if the node is not the same node and in same group
                    if identifier != idb and d['nodes'][idb]['group'] == 2:
                        # Get the current Euclidean distance for the current node i, to target node j
                        dst = euclidean(xa, ya, za, xb, yb, zb)
                        if j == layer2startid or dst < bestdst:
                            bestdst = dst
                            bestdstid = j
                        log += ('''<tr><th scope="row">''' + str(identifier)
                                + "</th><td>" + str(idb)
                                + "</td><td>" + str(px)
                                + "</td><td>" + str(py)
                                + "</td><td>" + str(pz)
                                + "</td><td>" + str(xa)
                                + "</td><td>" + str(ya)
                                + "</td><td>" + str(za)
                                + "</td><td>" + str(xb)
                                + "</td><td>" + str(yb)
                                + "</td><td>" + str(zb)
                                + "</td><td>" + str(dst)
                                + "</td><td>" + str(bestdst)
                                + "</td><td>" + str(bestdstid)
                                + '</td></tr>')
                d['links'].append({'puddleid': pid, 'source': i, 'target': bestdstid, 'euclidean': bestdst})

    if layer3puddlevisible == "on":
        d['links'].append({'puddleid': 3, 'source': 1, 'target': 8})  # Placeholder, delete later
    if layer4puddlevisible == "on":
        d['links'].append({'puddleid': 4, 'source': 1, 'target': 9})  # Placeholder, delete later
    if layer5puddlevisible == "on":
        d['links'].append({'puddleid': 5, 'source': 1, 'target': 10})  # Placeholder, delete later

    print('\n' + str(len(log)) + " characters added to log.\n")
    d['log'] = log

    try:
        with open("d3.json", "w") as d3_json_out:
            json.dump(d, d3_json_out, indent=4, sort_keys=False)
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return "Failed to open d3.json file."

def euclidean(xa, ya, za, xb, yb, zb):
    # tests on Matthew's computer ran math.hypot about 10-100x faster than scipy's function
    dst = math.hypot(xa - xb, ya - yb, za - zb)
    return dst
