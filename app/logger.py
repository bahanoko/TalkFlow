class TopicLogger:
    def __init__(self, window_size=3):
        self.window_size = window_size
        self.log: list[list[str]] = []

    def log_topics(self, topics: list[str]):
        self.log.append(topics)
        if len(self.log) > self.window_size:
            self.log.pop(0)

    def is_ready(self):
        return len(self.log) == self.window_size

    def get_log(self):
        return self.log.copy()

    def reset(self):
        self.log.clear()