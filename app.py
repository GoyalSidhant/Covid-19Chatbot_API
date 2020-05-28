from flask import Flask, jsonify, abort, make_response, request
import json
from model import response , responsive

app = Flask(__name__)


@app.route('/', methods=['POST'])
def get_bot_response():
    if not request.json or not 'message' in request.json:
        abort(400)
    print(request.json)
    print(type(request.json))
    temp = str(request.json)
    print(type(temp))
    temp = temp.replace("\'", "\"")
    parsed_json = json.loads(temp) 
    user_message = parsed_json['message']
    resp = str(response(user_message))
    return resp

if __name__ == "__main__":
    app.run() 