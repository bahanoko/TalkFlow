from flask import Flask, request, render_template, send_file
from extract import Extract
from logger import TopicLogger
from graph import TopicGraph
app = Flask(__name__)

logger = TopicLogger()
topic_graph = TopicGraph()
extractor = Extract(logger,topic_graph)
logger.set_extractor(extractor)

@app.route("/", methods=["GET", "POST"])
def index():
    received_text = None

    if request.method == "POST":
        received_text = request.form.get("text")
        extractor.extract_topics(received_text)

    return render_template("index.html")

@app.route('/graph')
def graph():
    return send_file('graph.html')


if __name__ == "__main__":
    app.run(debug=True)
