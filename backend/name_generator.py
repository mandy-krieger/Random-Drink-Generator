# -*- coding: utf-8 -*-
"""name_generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ACVc7Bh6Mzv8_IymlwgsNMNhXGibMgng
"""
from __future__ import unicode_literals, print_function, division
import torch 
import torch.nn as nn
from io import open
import glob
import os
import unicodedata
import string
import random

class RNN(nn.Module):
  def __init__(self, input_size, hidden_size, output_size):
    super(RNN, self).__init__()
    self.hidden_size = hidden_size

    self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
    self.i2o = nn.Linear(input_size + hidden_size, output_size)
    self.o2o = nn.Linear(hidden_size + output_size, output_size)
    self.dropout = nn.Dropout(0.1)
    self.softmax = nn.LogSoftmax(dim=1)

  def forward(self, input, hidden):
    combined = torch.cat((input, hidden), 1)
    hidden = self.i2h(combined)
    output = self.i2o(combined)
    output_combined = torch.cat((hidden, output), 1)
    output = self.o2o(output_combined)
    output = self.dropout(output)
    output = self.softmax(output)
    return output, hidden

  def initHidden(self):
    return torch.zeros(1, self.hidden_size)

letters = string.ascii_letters + string.digits + ".,;'-&! "
n_letters = len(letters) + 1

names = open("cocktailnames.txt").readlines()

for i, name in enumerate(names):
  names[i] = name[:-1]

def randomChoice(l):
    return l[random.randint(0, len(l) - 1)]

def inputTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li in range(len(line)):
        letter = line[li]
        tensor[li][0][letters.find(letter)] = 1
    return tensor

def targetTensor(line):
    letter_indexes = [letters.find(line[li]) for li in range(1, len(line))]
    letter_indexes.append(n_letters - 1) # EOS
    return torch.LongTensor(letter_indexes)

def getTraining():
  example = randomChoice(names)
  #print(example)
  input_line_tensor = inputTensor(example)
  target_line_tensor = targetTensor(example)
  return input_line_tensor, target_line_tensor

criterion = nn.NLLLoss()

learning_rate = 0.0005

def model_train(input_line_tensor, target_line_tensor):
  target_line_tensor.unsqueeze_(-1)
  hidden = rnn.initHidden()

  rnn.zero_grad()
  loss = 0

  for i in range(input_line_tensor.size(0)):
    output, hidden = rnn(input_line_tensor[i], hidden)
    l = criterion(output, target_line_tensor[i])
    loss += l

  loss.backward()

  for p in rnn.parameters():
    p.data.add_(p.grad.data, alpha=-learning_rate)
  
  return output, loss.item() / input_line_tensor.size(0)

import time
import math

def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

rnn = RNN(n_letters, 128, n_letters)

n_iters = 100000
print_every = 5000
plot_every = 500
all_losses = []
total_loss = 0 # Reset every plot_every iters

start = time.time()

for iter in range(1, n_iters + 1):
  input, target = getTraining()
  #print(target)
  output, loss = model_train(input, target)
  total_loss += loss

  if iter % print_every == 0:
      print('%s (%d %d%%) %.4f' % (timeSince(start), iter, iter / n_iters * 100, loss))

  if iter % plot_every == 0:
      all_losses.append(total_loss / plot_every)
      total_loss = 0

max_length = 20

def sample(start_letter="A"):
  with torch.no_grad():
    input = inputTensor(start_letter)
    hidden = rnn.initHidden()

    output_name = start_letter
    for i in range(max_length):
      output, hidden = rnn(input[0], hidden)
      topv, topi = output.topk(1)
      topi = topi[0][0]
      if topi == n_letters - 1:
          break
      else:
          letter = letters[topi]
          output_name += letter
      input = inputTensor(letter)
    
    return output_name

def random_sample(start_letters=list(string.ascii_uppercase)):
    start_letter = start_letters[random.randint(0,len(start_letters))]
    print(sample(start_letter))