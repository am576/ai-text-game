from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})
CORS(app, resources={r"/*":{'origins':"http://localhost:8080", "allow_headers": "Access-Control-Allow-Origins"}})

@app.route('/', methods=['GET'])
def index():
    return "The best ai driven text game in the universe"

if __name__ == "__main__":
    app.run(debug = True)