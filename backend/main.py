from flask import Flask, Response, request, send_file
from flask_cors import CORS, cross_origin
import requests
import json
from db.history import History
from comfy.generator import Generator

app = Flask(__name__)
CORS(app, origins='*')
app.config.from_object(__name__)
history = History()
generator = Generator()

CORS(app, resources={r"/*":{'origins':"http://localhost:8080"}})

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

@app.route('/generate_preview', methods=['POST'])
def generate_preview():
    prompt = request.json.get('prompt')
    preview =  generator.generateAdventurePreview(prompt)

    return  send_file(preview, mimetype='image/png')

@app.route('/save_adventure', methods=['POST'])
def save_adventure():
    type = request.json.get('type')
    name = request.json.get('name')
    description = request.json.get('description')
    history.addAdventure(type, name, description)
    return "Working"

if __name__ == "__main__":
    app.run(debug = True)
    