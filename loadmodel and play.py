import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from tron import *
from theagent import*
from tronrandomagent import *
import numpy as np
direct='agent1model'
env=trongame()
dqn=theagent()
ragent=randomagent()
dqn.loadmodel(direct)
count=0


env.agentagainstagent(dqn,ragent)

print("Eps {0:} winrate {1:.2f}".format(0,count/100))