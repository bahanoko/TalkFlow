from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from extract import GeminiAI
from logger import TopicLogger
from graph import TopicGraph
import threading
import time

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
    return {"status": "success"}, 200

@app.route("/graph", methods=["GET"])
def get_graph():
    result = topic_graph.get_result()
    if result:
        return jsonify(result)
    else:
        return jsonify({"status": "no graph"}), 404

@app.route("/reset", methods=["POST"])
def reset():
    logger.reset()
    topic_graph.reset()
    return {"status": "reset"}, 200

@socketio.on('connect')
def on_connect():
    print('クライアント接続')

def push_data():
    prev_result = None
    while True:
        result = topic_graph.get_result()
        if result != prev_result:
            socketio.emit('update', result if result else {"nodes": [], "links": []})
            prev_result = result
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=push_data, daemon=True).start()
    socketio.run(app, port=5000)