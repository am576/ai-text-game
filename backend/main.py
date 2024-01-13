from flask import Flask, Response, request, send_file, jsonify
from flask_cors import CORS, cross_origin
from comfy.generator import Generator
import json
from db.connection import MongoDBConnection
from db.models import Adventure
from game.game import Game

app = Flask(__name__)
CORS(app, origins='*')
app.config.from_object(__name__)
CORS(app, resources={r"/*":{'origins':"http://localhost:8080"}})

generator = Generator()
connection = MongoDBConnection()
game = None

@app.route('/', methods=['GET'])
def index():
    return "The best ai driven text game in the universe"
game = None
@app.route('/start_game', methods=['POST'])
def start_game():
    global game 
    adventure_id = request.json.get('adventure_id')
    game = Game(adventure_id)

    return "Ok"

@app.route('/load_game', methods=['POST'])
def load_game():
    global game 
    adventure_id = request.json.get('adventure_id')
    game = Game.load(adventure_id)

    return "Ok"

@app.route('/save_prompt', methods=['GET'])
def save_prompt():
    global game 
    prompt = request.args.get('prompt')
    game.addToHistory("user", prompt)
    return "Working"
    
@app.route('/save_response', methods=['POST'])
def save_response():
    global game 
    response = request.json.get('response')
    game.addToHistory("assistant", response)
    return "Working"

@app.route('/load_history', methods=['GET'])
def load_history():
    global game 
    return game.getHistory()


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
    adventure = json.loads(request.json.get('adventure'))
    character = adventure['character']
    name = adventure.get('name')
    description = adventure.get('worldDescription')
    character_description = character.get('description')
    avatar_description = adventure.get('avatarDescription')
    preview = generator.world_preview_path
    avatar = generator.avatar_preview_path
    
    if 'adventure_id' in request.get_json():
        adventure_id = request.json.get('adventure_id')
        if not preview:
            preview = f"../frontend/src/assets/adventures/{adventure_id}/preview.png"
        if not avatar:
            avatar = f"../frontend/src/assets/adventures/{adventure_id}/avatar.png"
        Adventure.save(adventure_id, name, description, character_description, avatar_description, preview, avatar)
    else:
        if not preview:
            preview = "../frontend/src/assets/placeholder_512.png"
        if not avatar:
            avatar = "../frontend/src/assets/placeholder_512.png"
        Adventure.create(name, description, character_description, avatar_description, preview, avatar)

    return "Working"

@app.route('/get_adventures', methods=['GET'])
def get_adventures():
    return Adventure.getAll()

@app.route('/get_adventure', methods=['GET'])
def get_adventure():
    adventure_id = request.args.get('id')

    return Adventure.get(adventure_id)

if __name__ == "__main__":
    app.run(debug = True)
