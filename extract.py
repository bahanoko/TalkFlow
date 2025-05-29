from google import genai
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
from graph import TopicGraph

class Extract:
    def __init__(self,logger,topic_graph):
        load_dotenv()
        self.key = os.getenv("GENAI_API_KEY")
        self.logger = logger
        self.topic_graph = topic_graph
        self.client = genai.Client(api_key=self.key)
        
    def extract_topics(self,talk):
        prompt = "From the following conversation, extract the current topic(s) as word(s) in Japanese.If the conversation relates to multiple topics, output all of them as a list."
        if talk == "":
            return
        prompt += talk
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": list[str],
            },
        )
        topics : list[str] = response.parsed
        if topics is None:
            return
        self.logger.log_topics(topics)

    def inference_graph(self,topics):
        class Relatedness(BaseModel):
            topic : str
            weight: float
        
        class TopicNode(BaseModel):
            topic: str
            related_topics: List[Relatedness]
        
        class TopicGraph(BaseModel):
            topics: List[TopicNode]

        prompt = (
            "Extract topics from the following text, and for each topic, extract related topics with relevance scores. "
            "Please output the result in the following JSON format:\n"
            '{ "topics": [ { "topic": "ex_topic1", "related_topics": [ '
            '{ "topic": "ex_topic2", "weight": 0.65 }, '
            '{ "topic": "ex_topic3", "weight": 0.54 } ] } ] }\n\n'
            f"Input topics: {topics}"
        )

        prompt += str(topics)

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents = prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": TopicGraph, 
            },
        )
        result = response.parsed
        self.topic_graph.topics_to_graph(result)

