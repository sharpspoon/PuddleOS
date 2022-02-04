import json


def createjson(layer1):
    json_file = "d3.json"
    # Create an empty new dict
    d = {'layer1': [], 'layer2': [], 'layer3': [], 'layer4': [], 'layer5': []}
    try:
        # Create the network.json file
        with open(json_file, 'r') as jsonfile:
            parsed = json.loads(jsonfile.read())

            nodes = []
            for n in parsed["layer1"]:
                nodes.append(n)
            for n in parsed["layer2"]:
                nodes.append(n)

            for node in parsed["links"]:
                d['nodes'].append({'id': node, 'group': 1})

            for node in parsed["nodes"]:
                d['nodes'].append({'id': node, 'group': 2})

                for link in parsed["nodes"][node]["links"]:
                    if link in nodes:
                        d['links'].append({'source': node, 'target': link, 'value': 1})

            with open(json_file, "w") as d3_json_out:
                json.dump(d, d3_json_out, indent=4, sort_keys=False)

            return "Build success."
    except Exception as e:
        print(e)
        return "Failed to open network.json file. Are you sure it is named correctly?"
