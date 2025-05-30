from google import genai
import os
from dotenv import load_dotenv
from models import TopicGraphModel
from typing import List

class GeminiAI:
    def __init__(self, logger, topic_graph):
        load_dotenv()
        self.key = os.getenv("GENAI_API_KEY")
        self.logger = logger
        self.topic_graph = topic_graph
        self.client = genai.Client(api_key=self.key)

    def extract_topics(self, talk: str):
        if not talk:
            return
        prompt = (
            "From the following conversation, extract the current topic(s) as word(s) in Japanese. "
            "If the conversation relates to multiple topics, output all of them as a list."
            + talk
        )
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": list[str],
            },
        )
        topics: List[str] = response.parsed
        if topics:
            self.logger.log_topics(topics)

    def inference_graph(self, topics: list[list[str]]):
        prompt = (
            "Extract topics from the following text, and for each topic, extract related topics with relevance scores. "
            "Please output the result in the following JSON format:\n"
            '{ "topics": [ { "topic": "ex_topic1", "related_topics": [ '
            '{ "topic": "ex_topic2", "weight": 0.65 }, '
            '{ "topic": "ex_topic3", "weight": 0.54 } ] } ] }\n\n'
            f"Input topics: {topics}"
        )
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": TopicGraphModel,
            },
        )
        result = response.parsed
        if result:
            self.topic_graph.topics_to_graph(result)

