from flask import Flask, request
from flask_socketio import SocketIO, emit
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
extractor = GeminiAI(logger, topic_graph)
logger.set_extractor(extractor)

@app.route("/send", methods=["POST"])
def index():
    received_text = request.form.get("text")
    extractor.extract_topics(received_text)
    print(received_text)
    return {"status": "success"}, 200

@app.route("/genarate",methods=["POST"])
def graph():
    if logger.log is None:
        return {"status": "failed"}, 400 #TODO: エラコ設定
    else :
        extractor.inference_graph(logger.log)
        return {"status": "success"}, 200
    
@socketio.on('connect')
def on_connect():
    print('クライアント接続')

def push_data():
    while True:
        socketio.emit('update', {'message': '最新データ', 'timestamp': time.time()})
        time.sleep(2)

if __name__ == '__main__':
    threading.Thread(target=push_data).start()
    socketio.run(app, port=5000)