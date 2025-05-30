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
            "From the following conversation, extract the current topic(s) as words or short phrases in Japanese. "
            "Include proper nouns such as names of anime, movies, games, or people, as well as important conversational keywords. "
            "If there are abbreviations or nicknames, please normalize them to their canonical (standard or full) names whenever possible. "
            "Only output topics that are explicitly mentioned or strongly implied in the conversation. "
            "Do not output any topics that are not referenced in the conversation.\n"
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
            if self.logger.is_ready():
                self.inference_graph(self.logger.get_log())

    def inference_graph(self, topics: list[list[str]]):
        prompt = (
            "You are given a list of topics extracted from a conversation. "
            "The list may include common terms, proper nouns such as names of anime, movies, games, or people, "
            "as well as important conversational keywords or phrases like 'favorite game'. "
            "Please include these key topics as nodes in the graph. "
            "Normalize all topics to their canonical (standard or full) names. "
            "For example, merge abbreviations or alternative names like '金銀' into their full name 'ポケモン金銀'. "
            "Do not treat variations or nicknames as separate topics.\n\n"
            "For each normalized topic, identify other clearly related topics from the list. "
            "Only include relationships that are explicitly mentioned or strongly implied by the context. "
            "Avoid speculative or generic connections.\n\n"
            "Output the result in the following JSON format:\n"
            '{\n'
            '  "topics": [\n'
            '    {\n'
            '      "topic": "ポケモン金銀",\n'
            '      "related_topics": [\n'
            '        { "topic": "ポケモン", "weight": 0.85 },\n'
            '        { "topic": "ゲームボーイ", "weight": 0.75 }\n'
            '      ]\n'
            '    },\n'
            '    {\n'
            '      "topic": "favorite game",\n'
            '      "related_topics": [\n'
            '        { "topic": "ポケモン金銀", "weight": 0.80 }\n'
            '      ]\n'
            '    },\n'
            '    ...\n'
            '  ]\n'
            '}\n\n'
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

