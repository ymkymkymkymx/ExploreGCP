import tensorflow as tf
from collections import deque
import numpy as np
import random
from tensorflow.keras.optimizers import Adam
class theagent:
    def __init__ (self):
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D( filters=1,kernel_size=2, activation='relu', input_shape=(60,60,1)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(120, activation='sigmoid'),
            tf.keras.layers.Dense(84, activation='sigmoid'),
            tf.keras.layers.Dense(4, activation='linear')
        ])
        self.model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
        self.target_model=tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(filters=1, kernel_size=2, activation='relu', input_shape=(60,60,1)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(120, activation='sigmoid'),
            tf.keras.layers.Dense(84, activation='sigmoid'),
            tf.keras.layers.Dense(4, activation='linear')
        ])
        self.target_model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
        self.target_model.set_weights(self.model.get_weights())
        self.memory=deque(maxlen=4000)
        self.episode=0
    def loadmemory(self,trans):
        self.memory.append(trans)
    def train(self,isepiend):
        if len(self.memory)<2000:
            return
        batch=random.sample(self.memory,1000)
        states=np.array([trans[0] for trans in batch])
        currentqlist=self.model.predict(states)
        newstates=np.array([trans[3] for trans in batch])
        newqlist=self.target_model.predict(newstates)
        x=[]
        y=[]
        
        for index,(state, action, reward, newcurrentstate,done) in enumerate(batch):
            if not done:
                maxfutureq= np.max(newqlist[index])
                newq = reward + 0.9 * maxfutureq
            else:
                newq =reward
            currentqs= currentqlist[index]
            currentqs[action] =newq
            
            x.append(state)
            y.append(currentqs)
        self.model.fit(np.array(x),np.array(y), verbose=0,shuffle=False)
        if isepiend:
            self.episode +=1
        if self.episode%4==3:
            self.target_model.set_weights(self.model.get_weights())
        
        
    def getqs(self, state):
        return self.model.predict(np.array([state]))[0]
    def savemodel(self,direct):
        self.model.save(direct)
    def loadmodel(self,direct):
        self.model.restore(direct)
        self.model.restore(direct)
    def predict(self,state):
        return np.argmax(self.model.predict(np.array([state]))[0])