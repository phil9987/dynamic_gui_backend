from flask import Flask, send_from_directory, request
import requests
from flask_cors import CORS
import xml.etree.ElementTree as ET


app = Flask(__name__)
CORS(app)

@app.route('/robotarmthing')
def robot_arm_thing():
    return send_from_directory('.', 'robotArmThing2.html')

@app.route('/sparql-extension/calendar')
def cal():
    return send_from_directory('.', 'calendar.txt')

@app.route('/sparql-extension/util')
def util():
    return send_from_directory('.', 'example.ldscript.txt')

@app.route('/call_linked_function', methods=['POST'])
def call_linked_function():
    payload = request.get_json()
    args_list = payload.get('args')
    args_str = ','.join(map(str, args_list))
    prefix, url = payload.get('linkedFunctionPrefix').split('|')
    function_name = payload.get('linkedFunction')
    function_str = "{}:{}({})".format(prefix, function_name, args_str)
    print("created linked function string: {}".format(function_str))
    sparql_request = f'''PREFIX {prefix}:<{url}> SELECT ?first ?second ?third ?fourth ?fifth ?sixth WHERE {{BIND ({function_str} AS ?list) BIND (xt:get(?list, 0) AS ?first) BIND (xt:get(?list, 1) AS second) BIND (xt:get(?list, 2) AS third) BIND (xt:get(?list, 3) AS fourth) BIND (xt:get(?list, 4) AS fifth) BIND (xt:get(?list, 5) AS sixth)}}'''
    headers = {'Content-type': 'application/sparql-query'}

    res = requests.post('http://lvh.me:8080/sparql', sparql_request, headers=headers)
    print(res.text)
    root = ET.fromstring(res.text)
    print('printing results')
    #print(ET.tostring(root, encoding='utf8').decode('utf8'))
    res_list = []
    for child in root:
        #print('parsing child')
        #print(child.tag, child.attrib)
        for cc in child:
            #print('parsing child of child')
            #print(cc.tag, cc.attrib)
            if cc.tag.endswith('result'):
                for ccc in cc:
                    #print('parsing child of child of child')
                    #print(ccc.tag, ccc.attrib)
                    for cccc in ccc:
                        print(cccc.text)
                        res_list.append(cccc.text)
    return str({"res":res_list})
