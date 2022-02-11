import json


def createjson(layer1, layer2, layer3, layer4, layer5):
    json_file = "d3.json"
    # Create an empty new dict
    d = {'layer1': [layer1], 'layer2': [layer2], 'layer3': [layer3], 'layer4': [layer4], 'layer5': [layer5]}
    try:
        with open(json_file, "w") as d3_json_out:
            json.dump(d, d3_json_out, indent=4, sort_keys=False)

        return
    except Exception as e:
        print(e)
        return "Failed to open network.json file. Are you sure it is named correctly?"
