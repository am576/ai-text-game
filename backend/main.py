from flask import Flask, Response, request
from flask_cors import CORS
import requests
import json
from db.history import History

app = Flask(__name__)
app.config.from_object(__name__)
history = History()

CORS(app, supports_credentials=True)
CORS(app, resources={r"/*":{'origins':"*"}})
CORS(app, resources={r"/*":{'origins':"http://localhost:8080", "allow_headers": "Access-Control-Allow-Origins"}})

@app.route('/', methods=['GET'])
def index():
    return "The best ai driven text game in the universe"

@app.route('/prompt', methods=['GET'])
def prompt():
    prompt = request.args.get('prompt')
    print('Asking ai ', prompt)
    history.addToHistory("user", prompt)
    # url = 'http://localhost:11434/api/generate'
    chat_history = history.getHistory()
    print(chat_history)
    url = 'http://localhost:11434/api/chat'
    data = chat_history
    response = requests.post(url, json=data, stream=True)
    
    print("Response is ", response.text)
    def generate_stream():
        for line in response.iter_lines():
            string_line = line.decode('utf-8')
            line = json.loads(string_line)
            value = line.get("content")
            done = line.get("done")

            if value:
                yield f"data: {value}\n\n"
            if done:
                yield f"data: The AI has completed generation\n\n"
                return
                yield f"data: {done}\n\n"
    res = Response(generate_stream(), mimetype='text/event-stream')
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.route('/save_response', methods=['GET'])
def save_response():
    response = request.args.get('response')
    history.addToHistory("assistant", response)

if __name__ == "__main__":

    app.run(debug = True)
    