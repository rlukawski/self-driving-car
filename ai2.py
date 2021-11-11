# AI For self driving car

# libraries

import numpy as np
import random
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable

class Network(nn.Module):
    def __init__(self, input_size, ):
        super(Network,self).__init__()
        self.input_size = input_size
        self.nb_action = nb_action 
        self.fc1 = nn.Linear(input_size, 30)
        self.fc2 = nn.Linear(30, nb_action)
        
    def forward(self, state):
        X = F.relu(self.fc1(state))
        q_values = self.fc2(X)
        return q_values
    
# Implementing Experience Replay

class ReplayMemory(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        
    def push(self, event):
        self.memory.append(event)
        if len(self.memory) > self.capacity:
            del self.memory[0]
            
            
    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size))
        return map(lambda x: Variable(torch.cat(x,0)), samples)
    
class Dqn():
    def __init(self, input_size, nb_action, gamma):
        self.gamma = gamma
        self.reward_window = []
        self.model = Network(input_size, nb_action)
        
        self.memory = ReplayMemory(100000)
        
        self.optimizer = optim.Adam(self.model.parameters(), lr = 0.001)
        
        self.last_state = torch.Tensor().unsqueeze(0)
        self.last_action = 0
        self.last_reward = 0
        
    def select_action(self, state):
        probs = F.softmax(self.model(Variable(state, volatile = True)) * 7) # T=7
        # softmax([1,2,3]) = [0.04, 0.11, 0.85] => softmax([1,2,3]* 3) = [0,0.02,0.98]
        action = probs.multinomial()
        return action.data[0,0]
    
    def learn(self, batch_state, batch_next_state, batch_reward, batch_action):
        outputs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)
        next_outputs = self.model(batch_next_state).detach().max(1)[0]
        
        
            
            
            
        