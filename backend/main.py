from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
import requests
import json
from db.history import History

app = Flask(__name__)
CORS(app, origins='*')
app.config.from_object(__name__)
history = History()

# CORS(app, supports_credentials=True)
CORS(app, resources={r"/*":{'origins':"*"}})
CORS(app, resources={r"/*":{'origins':"http://localhost", "allow_headers": "Access-Control-Allow-Origins"}})

@app.route('/', methods=['GET'])
def index():
    return "The best ai driven text game in the universe"

@app.route('/save_prompt', methods=['GET'])
def save_prompt():
    prompt = request.args.get('prompt')
    print('Asking ai ', prompt)
    history.addToHistory("user", prompt)
    return "Working"
    

@app.route('/save_response', methods=['POST'])
def save_response():
    response = request.json.get('response')
    history.addToHistory("assistant", response)
    return "Working"

@app.route('/load_history', methods=['GET'])
def load_history():
    return history.getHistory()



if __name__ == "__main__":
    app.run(debug = True)
    