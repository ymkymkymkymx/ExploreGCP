
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
currentstate=env.board.copy()
for i in range(100):
    currentstate=env.board.copy()
    done= False
    while not done:
        p1move=dqn.predict(currentstate)
        p2move=ragent.predict(currentstate)
        newstate,rewards =env.step(p1move,p2move)
        if rewards!=(0,0):
            done=True
        reward=rewards[0]
        dqn.loadmemory((currentstate,p1move,reward,newstate,done))
        dqn.train(done)
        currentstate=newstate
    env.restart()
    if i%2==0:
        print("{0:d} episodes finished,{1:d} samples in batch".format(i,len(dqn.memory)))
    
    if i%10==0:
        count=0
        for j in range(100):
            env.restart()
            currentstate=env.board.copy()
            while not done:
                p1move=dqn.predict(currentstate)
                p2move=ragent.predict(currentstate)
                newstate,rewards =env.step(p1move,p2move)
                if rewards!=(0,0):
                    if rewards[0]==1:
                        count+=1
                    done=True
                currentstate=newstate 
        env.restart()
        env.agentagainstagent(dqn,ragent)
        env.restart()
        print("Eps {0:} winrate {1:.2f}".format(i,count/100))
dqn.savemodel(direct)