class TopicLogger:
    def __init__(self):
        self.depth = 0
        self.log: list[list[str]] = [None] * 3
        self.extractor = None

    def set_extractor(self, extractor):
        self.extractor = extractor

    def log_topics(self, topics: list[str]):
        self.log[self.depth] = topics
        self.depth += 1
        if self.depth % 3 == 0:
            self.depth = 0