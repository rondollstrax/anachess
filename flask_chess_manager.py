import tensorflow_chessbot

class Args(object):
    def __init__(self, url=None, filepath=None):
        self.url = url
        self.filepath = filepath

def run_chessbot_with_image(imagepath):
    args = Args(filepath=imagepath)
    tensorflow_chessbot.main(args)
    return tensorflow_chessbot.return_fen()
