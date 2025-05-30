from pydantic import BaseModel
from typing import List

class Relatedness(BaseModel):
    topic: str
    weight: float

class TopicNode(BaseModel):
    topic: str
    related_topics: List[Relatedness]

class TopicGraphModel(BaseModel):
    topics: List[TopicNode]