from pathlib import Path
import sys
main_path = Path(__file__).parent.parent
sys.path.append(str(main_path))
from flask import Flask, request, jsonify
from main import decrypt, KEY, KEY_BYTES
from dotenv import load_dotenv
import json

load_dotenv()

DIR_JSON = Path(__file__).parent.parent / 'dump.json'

API_KEY = 'AB_4g1dhJvysdrfR9HPax49hjYh2nv5UhjqbMz5a2RMG1'

app = Flask(__name__)

@app.route('/')
def homepage() :
    home = {
        'message': 'API is running',
        'status': 'OK'
    }
    return jsonify(home)

def check_token():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorizad'}), 401
    
    token = auth_header.split(' ', 1)[1]

    if token != API_KEY:
        return jsonify({'error', 'Invalid API Key'}), 403

def decrypt_json_dump():
    with open(DIR_JSON, 'r') as file:
        a = file.read()
        b = decrypt(a, KEY_BYTES).decode('utf-8')
        return b

@app.route('/<product>', methods=['GET'])
def list_all(product):
    erro = check_token()
    if erro:
        return erro
    decrypt_json = decrypt_json_dump()
    list_all = json.loads(decrypt_json)
    return jsonify([{"id": id, **info} for id, info in list_all.get(product, {}).items()])

@app.route('/<product>/<int:id>', methods=['GET'])
def list_one(product, id):
    erro = check_token()
    if erro:
        return erro
    decrypt_json = decrypt_json_dump()
    list_all = json.loads(decrypt_json)
    product_dict = list_all.get(product, {})
    product_info = product_dict.get(str(id))
    if product_info is None:
        return jsonify({'error': 'id inválido'}), 401
    return jsonify({"id": str(id), **product_info})

@app.route('/<product>/<int:id>', methods=['PUT'])
def edit_one(product, id):
    erro = check_token()
    if erro:
        return erro
    decrypt_json = decrypt_json_dump()
    list_all = json.loads(decrypt_json)
    response = request.get_json()
    product_dict = list_all.get(product, {})
    product_info = product_dict.get(str(id))
    if product_info is None:
        return jsonify({'error': 'invalid id.'}), 401
    product_info.update(response)
    return jsonify({"id": str(id), **product_info})

@app.route('/<product>/<int:id>', methods=['DELETE'])
def delete_one(product, id):
    erro = check_token()
    if erro:
        return erro
    decrypt_json = decrypt_json_dump()
    list_all = json.loads(decrypt_json)
    product_dict = list_all.get(product, {})
    product_info = product_dict.get(str(id))
    if product_info is None:
        return jsonify({'error': 'invalid id.'}), 401
    del product_info
    return jsonify({'lista_tv': product_dict})

@app.route('/<product>/<int:id>', methods=['POST'])
def create_one(product, id):
    erro = check_token()
    if erro:
        return erro
    decrypt_json = decrypt_json_dump()
    list_all = json.loads(decrypt_json)
    product_dict = list_all.get(product, {})
    response = request.get_json()
    for i in product_dict:
        if str(id) in i:
            return jsonify({'error': 'existing id.'}), 401
    product_dict[str(id)] = response
    list_all[product] = product_dict
    return jsonify({"id": str(id), **product_dict})

app.run()