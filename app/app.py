from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from gemini import GeminiAI
from logger import TopicLogger
from graph import TopicGraph

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

logger = TopicLogger()
topic_graph = TopicGraph()
gemini = GeminiAI(logger, topic_graph)

@app.route("/send", methods=["POST"])
def index():
    received_text = request.form.get("text")
    gemini.extract_topics(received_text)
    result = topic_graph.get_result()
    socketio.emit('update', result if result else {"nodes": [], "links": []})
    return {"status": "success"}, 200

@app.route("/reset", methods=["POST"])
def reset():
    logger.reset()
    topic_graph.reset()
    socketio.emit('update', {"nodes": [], "links": []}) 
    return {"status": "reset"}, 200

@socketio.on('connect')
def on_connect():
    print('クライアント接続')

if __name__ == '__main__':
    socketio.run(app, port=5000)