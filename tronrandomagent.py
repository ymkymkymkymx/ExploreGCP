from tron import *
import random
class randomagent:
    def predict(self,board):
        return  random.randint(1,4)
    
if __name__ == "__main__":
    game=trongame()
    game.humanagainstagent(randomagent)