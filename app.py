import json
import math
import random
from datetime import date
from tracemalloc import start
from uuid import uuid4
from flask import Flask, render_template, request, redirect, url_for, send_file, session
import database
from pprint import pprint


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

# if true, will use MongoDB for user data
# if false, will use local file d3.json
USE_DATABASE = False


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():     
    data = getUserData()
    layers = data['layers']

    layers_count = len(layers)
    layer_totals = [layer['total'] for layer in layers]
    totalnodes = sum(layer_totals)

    layer_colors = [layer['color'] for layer in layers]
    layer_sizes = [layer['size'] for layer in layers]

    result = lambda x: "checked" if x == "on" else ""
    layer_displays = [result(x["visible"]) for x in layers]

    result = lambda x: "checked" if x == "on" else ""
    layer_puddle_displays = [result(x["puddle_visible"]) for x in layers]

    layer_clusterings = [buildclusteringhtml(x["clustering"]) for x in layers]

    try:
        return render_template('index.html',
                               nodedata=data['nodes'],
                               year=date.today().year,
                               x=data['x'],
                               y=data['y'],
                               z=data['z'],
                               layer_displays=layer_displays,
                               layer_puddle_displays=layer_puddle_displays,
                               layer_clusterings=layer_clusterings,
                               layers_count = layers_count,
                               layer_totals = layer_totals,
                               layer_colors = layer_colors,
                               layer_sizes = layer_sizes,
                               totalnodes=totalnodes)
    except Exception as e:
        print(e)
        return render_template('index.html')

@app.route("/log", methods=["GET"])
def log():
    data = getUserData()
    return render_template('log.html',
                           year=date.today().year,
                           log=data['log'])


@app.route("/nodedata", methods=["GET"])
def nodedata():
    data = getUserData()
    return render_template('nodedata.html',
                           year=date.today().year,
                           nodedata=data['nodes'])


@app.route("/linkdata", methods=["GET"])
def linkdata():     
    data = getUserData()
    return render_template('linkdata.html',
                           year=date.today().year,
                           linkdata=data['links'])


@app.route("/d3json", methods=["GET"])
def d3json():
    if USE_DATABASE:
        return json.dumps(getUserData())
    else:
        return send_file('sample.json')


@app.route("/d3js", methods=["GET"])
def graphjs():
    return send_file('d3.js')


def buildclusteringhtml(method):
    ret = ""
    if method == "Agglomerative Complete Linkage Hierarchical Clustering":
        ret = '''<option value="Agglomerative Complete Linkage Hierarchical Clustering" selected>Agglomerative Complete Linkage Hierarchical Clustering</option>
        <option value="DBSCAN">DBSCAN</option>'''
    elif method == "DBSCAN":
        ret = '''<option value="Agglomerative Complete Linkage Hierarchical Clustering">Agglomerative Complete Linkage Hierarchical Clustering</option>
        <option value="DBSCAN" selected>DBSCAN</option>'''
    return ret


@app.route("/createjson", methods=["POST"])
def createjson():
    # Get all form values on submission.
    global nodecountchange
    nodecountchange = False
    layer_count = int(request.form.get("layer_count"))
    layer_nodes_count = [int(request.form.get(f'layer{i}')) for i in range(1, layer_count + 1)]

    layer_colors = [request.form.get(f'colorInput{i}') for i in range(1, layer_count + 1)]

    layer_sizes = [int(request.form.get(f"layer{i}size")) for i in range(1, layer_count + 1)]

    layer_visibiled_raw = [request.form.get(f"nodeDisplay{i}") for i in range(1, layer_count + 1)]

    layer_clusterings = [request.form.get(f"layer{i}ClusteringMethod") for i in range(1, layer_count + 1)]

    layer_puddle_visibile_raw = [request.form.get(f"puddleDisplay{i}") for i in range(1, layer_count + 1)]

    randomize_layer =  [request.form.get(f"randomizeLayer{i}") for i in range(1, layer_count + 1)]

    x = request.form.get("x")
    y = request.form.get("y")
    z = request.form.get("z")

    # This logic is for setting the individual nodes to visible or hidden
    result = lambda x : "visible" if x == "on" else "hidden"
    layer_visibiled = [result(i) for i in layer_visibiled_raw]

    # This logic is for setting the puddles to visible or hidden
    result = lambda x : "visible" if x == "on" else "hidden"
    layer_puddle_visibiled = [result(i) for i in layer_puddle_visibile_raw]

    totalnodes = sum(layer_nodes_count)
    layer_i_startid = [sum(layer_nodes_count[:i]) for i in range(layer_count)]
    xint = int(x)
    yint = int(y)
    zint = int(z)
    log = ""

    result = {'x': xint,
         'y': yint,
         'z': zint,
         'layers': [],
         'nodes': [],
         'links': [],
         'log': log}

    original_data = getUserData()
    data_layer_totals = [a['total'] for a in original_data['layers']]
    if data_layer_totals != layer_nodes_count:
        nodecountchange = True
    print(f"nodecountchange: {nodecountchange}")

    for layer_i in range(layer_count):
        new_layer = {
            'layerNumber' : layer_i+1,
            'name' : f"layer{layer_i+1}",
            'total' : layer_nodes_count[layer_i],
            'color' : layer_colors[layer_i],
            'size' : layer_sizes[layer_i],
            'visible' : layer_visibiled_raw[layer_i],
            'clustering' : layer_clusterings[layer_i],
            'puddle_visible' : layer_puddle_visibile_raw[layer_i],
        }
        result['layers'].append(new_layer)

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

    nodes_by_group = [[] for _ in range(layer_count+1)]
    g = -1
    for layer_i in range(layer_count):
        for i in range(layer_nodes_count[layer_i]):
            g += 1
            if nodecountchange is True or randomize_layer[layer_i] == "on":
                curr_node = newNode(g, layer_i+1, layer_sizes[layer_i], layer_colors[layer_i], layer_visibiled[layer_i])
                result['nodes'].append(curr_node)
                nodes_by_group[layer_i+1].append(curr_node)
            else:
                curr_node = original_data['nodes'][layer_i_startid[layer_i] + i]
                x, y, z = map(int, (curr_node['fx'], curr_node['fy'], curr_node['z']))
                curr_node = newNode(g, layer_i+1, layer_sizes[layer_i], layer_colors[layer_i], layer_visibiled[layer_i], x, y, z)
                result['nodes'].append(curr_node)
                nodes_by_group[layer_i+1].append(curr_node)

    pid = 1  # Set the PuddleId to 0
    for layer_i in range(layer_count):
        if layer_puddle_visibiled[layer_i] == 'visible':
            for node in nodes_by_group[layer_i+1]:

                # =============== Not really sure why this is needed ===================== #
                # I think this is fine?
                i_tmp = node['id']

                # If this previous node is in the same group
                if result['nodes'][i_tmp - 1]['group'] == layer_i+1:  
                    px = result['nodes'][i_tmp - 1]['fx']
                    py = result['nodes'][i_tmp - 1]['fy']
                    pz = result['nodes'][i_tmp - 1]['z']
                else:  
                    # There is no previous node in this group.
                    px = None
                    py = None
                    pz = None
                # ======================================================================== #

                # Get info for current node
                x_0, y_0, z_0 = node['fx'], node['fy'], node['z']
                id_0 = node['id']
                best_dst = float('inf')
                best_dst_id = -1

                # Iterate through all other nodes in the same group to find closest
                for node_b in nodes_by_group[layer_i+1]:
                    if node_b['id'] == id_0:
                        continue

                    x_1, y_1, z_1 = node_b['fx'], node_b['fy'], node_b['z']
                    id_1 = node_b['id']

                    # SQRT not needed since we only care about being smallest
                    dst = (x_1-x_0)**2 + (y_1-y_0)**2 + (z_1-z_0)**2
                    if dst < best_dst:
                        best_dst = dst
                        best_dst_id = id_1

                    # Add to log -- more pythonic way to concatenate a bunch of strings without newlines between them
                    log += (f'<tr><th scope="row">{id_0}</th>'
                    f'<td>{id_1}</td>'
                    f'<td>{px}</td>'
                    f'<td>{py}</td>'
                    f'<td>{pz}</td>'
                    f'<td>{x_0}</td>'
                    f'<td>{y_0}</td>'
                    f'<td>{z_0}</td>'
                    f'<td>{x_1}</td>'
                    f'<td>{y_1}</td>'
                    f'<td>{z_1}</td>'
                    f'<td>{math.sqrt(dst)}</td>'
                    f'<td>{math.sqrt(best_dst)}</td>'
                    f'<td>{best_dst_id}</td>'
                    '</tr>'
                    )

                result['links'].append({'puddleid': pid, 'source': id_0, 'target': best_dst_id, 'euclidean': math.sqrt(best_dst)})
                pid += 1
                



    # if layer1puddlevisible == "on":
    #     d['links'].append({'puddleid': 1, 'source': 1, 'target': 6})  # Placeholder, delete later

    # if layer2puddlevisible == "on":
    #     for i in range(layer2startid, layer2startid + layer2nodes):
    #         # Get the node at the current index
    #         node_a = d['nodes'][i]
    #         if node_a['group'] == 2:  # If the current node is in group 2.
    #             pid += 1  # Increase the Puddle ID by 1 each time.

    #             # Set the previous, source, and destination x, y, z variables
    #             if d['nodes'][i - 1]['group'] == 2:  # If this previous node is in the same group
    #                 px = d['nodes'][i - 1]['fx']
    #                 py = d['nodes'][i - 1]['fy']
    #                 pz = d['nodes'][i - 1]['z']
    #             else:  # There is no previous node in this group.
    #                 px = None
    #                 py = None
    #                 pz = None

    #             xa = node_a['fx']
    #             ya = node_a['fy']
    #             za = node_a['z']

    #             identifier = d['nodes'][i]['id']
    #             bestdst = float('inf')
    #             bestdstid = None

    #             # For this current node, loop through all other nodes and find closest
    #             for j in range(layer2startid, layer2startid + layer2nodes):
    #                 # Set the current destination node location
    #                 node_b = d['nodes'][j]
    #                 xb = node_b['fx']
    #                 yb = node_b['fy']
    #                 zb = node_b['z']
    #                 idb = node_b['id']

    #                 # Only proceed if the node is not the same node and in same group
    #                 if identifier != idb and d['nodes'][idb]['group'] == 2:
    #                     # Get the current Euclidean distance for the current node i, to target node j
    #                     dst = euclidean(xa, ya, za, xb, yb, zb)
    #                     if j == layer2startid or dst < bestdst:
    #                         bestdst = dst
    #                         bestdstid = j
    #                     log += ('''<tr><th scope="row">''' + str(identifier)
    #                             + "</th><td>" + str(idb)
    #                             + "</td><td>" + str(px)
    #                             + "</td><td>" + str(py)
    #                             + "</td><td>" + str(pz)
    #                             + "</td><td>" + str(xa)
    #                             + "</td><td>" + str(ya)
    #                             + "</td><td>" + str(za)
    #                             + "</td><td>" + str(xb)
    #                             + "</td><td>" + str(yb)
    #                             + "</td><td>" + str(zb)
    #                             + "</td><td>" + str(dst)
    #                             + "</td><td>" + str(bestdst)
    #                             + "</td><td>" + str(bestdstid)
    #                             + '</td></tr>')
    #             d['links'].append({'puddleid': pid, 'source': i, 'target': bestdstid, 'euclidean': bestdst})

    # if layer3puddlevisible == "on":
    #     d['links'].append({'puddleid': 3, 'source': 1, 'target': 8})  # Placeholder, delete later
    # if layer4puddlevisible == "on":
    #     d['links'].append({'puddleid': 4, 'source': 1, 'target': 9})  # Placeholder, delete later
    # if layer5puddlevisible == "on":
    #     d['links'].append({'puddleid': 5, 'source': 1, 'target': 10})  # Placeholder, delete later

    print('\n' + str(len(log)) + " characters added to log.\n")
    result['log'] = log

    if USE_DATABASE:
        database.update_user_data(session['uuid'],result)
    else:
        try:
            with open("new_sample.json", "w") as d3_json_out:
                json.dump(result, d3_json_out, indent=4, sort_keys=False)
        except Exception as e:
            print(e)
            return "Failed to open new_sample.json file."

    return redirect(url_for('index'))


def euclidean(xa, ya, za, xb, yb, zb):
    # tests on Matthew's computer ran math.hypot about 10-100x faster than scipy's function
    dst = math.hypot(xa - xb, ya - yb, za - zb)
    return dst

def getUserData():
    if USE_DATABASE:
        if 'uuid' not in session:
            session['uuid'] = uuid4()
            database.create_user_data(session['uuid'])
        return database.get_user_data(session['uuid'])
    else:
        data = None
        try:
            with open("sample.json") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Data json not found, exiting...")
            exit(1)
        return data
