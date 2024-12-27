import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game import Brasopolis

if __name__ == "__main__":
    game = Brasopolis()
    game.run()
