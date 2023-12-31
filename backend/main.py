from flask import Flask, Response, request, send_file, jsonify
from flask_cors import CORS, cross_origin
from db.history import History
from comfy.generator import Generator
import json

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

@app.route('/world_preview', methods=['POST'])
def world_preview():
    prompt = request.json.get('prompt')
    world_prompt = "3d fantasy digital illustration of " + prompt
    preview =  generator.generateWorldPreview(world_prompt)

    return  send_file(preview, mimetype='image/png')

@app.route('/avatar_preview', methods=['POST'])
def avatar_preview():
    prompt = request.json.get('prompt')
    avatar_prompt = "3d fantasy digital portrait of character " + prompt
    preview =  generator.generateAvatarPreview(avatar_prompt)

    return  send_file(preview, mimetype='image/png')

@app.route('/save_adventure', methods=['POST'])
def save_adventure():
    # type = request.json.get('type')
    adventure = json.loads(request.json.get('adventure'))
    character = adventure['character']
    name = adventure.get('name')
    description = adventure.get('worldDescription')
    character_description = character.get('description')
    avatar_description = adventure.get('avatarDescription')
    preview = generator.world_preview_path
    avatar = generator.avatar_preview_path
    if not preview:
        preview = "../frontend/src/assets/placeholder_512.png"
    if not avatar:
        avatar = "../frontend/src/assets/placeholder_512.png"
    
    history.addAdventure(name, description, character_description, avatar_description, preview, avatar)
    
    return "Working"

@app.route('/get_adventures', methods=['GET'])
def get_adventures():
    return jsonify(history.getAdventures())

if __name__ == "__main__":
    app.run(debug = True)
    