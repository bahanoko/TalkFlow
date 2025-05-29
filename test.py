from typing import List
from dataclasses import dataclass

@dataclass
class Relatedness:
    topic: str
    weight: float

@dataclass
class TopicNode:
    topic: str
    related_topics: List[Relatedness]

topics: List[TopicNode] = [
    TopicNode(topic='USJ', related_topics=[
        Relatedness(topic='ホグワーツ城', weight=0.8),
        Relatedness(topic='バタービール', weight=0.3),
        Relatedness(topic='ジュラシックパーク', weight=0.2),
        Relatedness(topic='スヌーピー', weight=0.15),
        Relatedness(topic='ディズニー', weight=0.4),
    ]),
    TopicNode(topic='ホグワーツ城', related_topics=[
        Relatedness(topic='USJ', weight=0.8),
        Relatedness(topic='バタービール', weight=0.6),
    ]),
    TopicNode(topic='バタービール', related_topics=[
        Relatedness(topic='ジュラシックパーク', weight=0.4),
        Relatedness(topic='スヌーピー', weight=0.3),
        Relatedness(topic='USJ', weight=0.3),
        Relatedness(topic='ホグワーツ城', weight=0.6),
    ]),
    TopicNode(topic='ジュラシックパーク', related_topics=[
        Relatedness(topic='バタービール', weight=0.4),
        Relatedness(topic='スヌーピー', weight=0.7),
    ]),
    TopicNode(topic='スヌーピー', related_topics=[
        Relatedness(topic='バタービール', weight=0.3),
        Relatedness(topic='ジュラシックパーク', weight=0.7),
    ]),
    TopicNode(topic='ディズニー', related_topics=[
        Relatedness(topic='USJ', weight=0.4),
    ]),
]

print(topics)
    

