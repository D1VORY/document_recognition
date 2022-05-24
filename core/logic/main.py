import cv2


class Word:
    def __init__(self, rectangle):
        self.rectangle = rectangle
        self.word = self.get_word()

    def get_word(self):
        return 'word'


