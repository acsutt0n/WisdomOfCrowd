# show survey data

import loadConfData as lCD
import sys
import pylab as py
import numpy as np
from scipy import stats
import math
import itertools as it


answers = [0,1,0,0,1,1,1,1,1,0,1,0,1,1,1,1]




def trunc(ary):
  # truncate to 3 decimals
  new_ary = [float('%0.3f' %i) for i in ary]
  return new_ary



def sortAndReturn(col0, col1, op=1):
  # sorts arrays and keeps members in place, 1 = descnd, 0 = ascend
  col0 = np.array(col0)
  col1 = np.array(col1)
  if op == 1:
    col2 = col0[col0.argsort()][::-1]
    col3 = col1[col0.argsort()][::-1]
  elif op == 0:
    col2 = col0[col0.argsort()]
    col3 = col1[col0.argsort()]
  
  return col2, col3
  



def getMatrix(AllData):
  # create matrices for all the data
  numQs = len(AllData.keys())
  subjects = 12    #len(AllData[1]['RT'])
  correct = np.array(py.zeros([numQs, subjects]))
  confA = np.array(py.zeros([numQs, subjects]))
  confB = np.array(py.zeros([numQs, subjects]))
  RTs = np.array(py.zeros([numQs, subjects]))
  #print(AllData)
  for i in xrange(subjects):
    # rows
    for j in xrange(1,17):
      # columns
      correct[j-1,i] = AllData[j]['correct'][i]
      
  for i in xrange(subjects):
    for j in xrange(1,17):
      confA[j-1,i] = AllData[j]['confA'][i]
  for i in xrange(subjects):
    for j in xrange(1,17):
      confB[j-1,i] = AllData[j]['confB'][i]
  for i in xrange(subjects):
    for j in xrange(1,17):
      RTs[j-1,i] = AllData[j]['RT'][i]
  
  print(py.shape(correct), py.shape(confA), py.shape(confB), py.shape(RTs))
  return correct, confA, confB, RTs




def groupConfidence(AllData):
  """
  treat all data as group
  """
  correct, confA, confB, RTs = getMatrix(AllData)
  
  answ = [1.5,2,3,4,5.5,6.5,7.5,8.5,9.5,10,11.5,12,13.5,14.5,15.5,16.5]
  hundy = py.ones(len(answ))
  hundy = hundy*50
  fig = py.figure()
  ax1 = fig.add_subplot(111)
  m,n = py.shape(correct)
  ANS0 = []
  ANS1 = []
  for i in range(m):
    ans0, ans1 = [], []
    for j in range(n):
      ans0.append(confA[i,j])
      ans1.append(confB[i,j])
    ANS0.append(py.sum(ans0))
    ANS1.append(py.sum(ans1))
  
  # get democratic % correct
  collective = []
  for i in range(len(ANS0)):
    if ANS0[i] > ANS1[i]:
      collective.append(0)
    else:
      collective.append(1)
  right = []
  print(len(collective))
  for i in range(len(answers)):
    if collective[i] == answers[i]:
      right.append(1)
    else:
      right.append(0)
  colmean = py.mean(right)
  print('Collective mean: %.3f' % colmean)
  
  
  prange = range(1,17)
  prange2 = [prange[i]+0.25 for i in range(len(prange))]
  # print(ANS0, ANS1)
  rects0 = ax1.bar(prange, ANS0, color='b', width=0.35)
  rects1 = ax1.bar(prange2, ANS1, color='r', width=0.35)
  ax1.set_title('Democratic decisions')
  ax1.set_xlabel('Question No.')
  ax1.set_ylabel('Confidence')
  ax1.plot(answ, hundy, 'k*')
  
    



def indConfidence(AllData):
  """
  treat as individuals
  """
  correct, confA, confB, RTs = getMatrix(AllData)
  
  fig = py.figure()
  ax2 = fig.add_subplot(111)
  m,n = py.shape(correct)
  answ = [1.5,2,3,4,5.5,6.5,7.5,8.5,9.5,10,11.5,12,13.5,14.5,15.5,16.5]
  hundy = py.ones(len(answ))
  hundy = hundy*8
  
  ANS0 = []
  ANS1 = []
  for i in range(m):
    ans0, ans1 = [], []
    for j in range(n):
      if correct[i,j] == 1:
        ans1.append(1)
      elif correct[i,j] == 0:
        ans0.append(1)
    ANS0.append(py.sum(ans0))
    ANS1.append(py.sum(ans1))
  
  # get individual mean
  means = []
  for i in range(n):
    means.append(py.mean(correct[:,i]))
  
  print('Individual mean: %.3f' % py.mean(means))
  
  
  prange = range(1,17)
  prange2 = [prange[i]+0.25 for i in range(len(prange))]
  # print(ANS0, ANS1)
  rects0 = ax2.bar(prange, ANS0, color='b', width=0.35)
  rects1 = ax2.bar(prange2, ANS1, color='r', width=0.35)
  ax2.set_title('Every man is an island')
  ax2.set_xlabel('Question No.')
  ax2.set_ylabel('Confidence')
  ax2.plot(answ, hundy, 'k*')




def moreConfident(AllData):
  """
  this compares the group response to the individual based on
  the confidence difference -- how much 'righter' is the group
  on average versus for questions with high confidence?
  answers = [0,1,0,0,1,1,1,1,1,0,1,0,1,1,1,1]
  """
  correct, confA, confB, RTs = getMatrix(AllData)
  conf_spread = []
  m, n = py.shape(confA)
  for i in xrange(m):
    for j in xrange(n):
      conf_spread.append(abs(confA[i,j] - confB[i,j]))
  med = np.median(conf_spread)
  
  # for each question determine the level of confidence
  cconf = []
  for i in xrange(m):
    current_conf = []
    for j in xrange(n):
      if answers[i] == 0:
        current_conf.append(confA[i,j] - confB[i,j])
      elif answers[i] == 1:
        current_conf.append(confB[i,j] - confA[i,j])
    cconf.append(sum(current_conf))
  print(answers)
  print(cconf)
  
  correcto = [ # cconf[positive]/cconf[total]
  
  fig = py.figure()
  ax3 = fig.add_subplot(111)
  ax3.hist(conf_spread, bins=20)
  
  
  




def showDataControl(answerFile, version=1):
  """
  run the plotting functions and display the data
  """
  # load answer data from lSD program
  #print('control called')
  AllData, AllInfo = lCD.answerControl(answerFile, 0)
  
  if version==1:
    groupConfidence(AllData)
  
  elif version==0:
    indConfidence(AllData)
    groupConfidence(AllData)
    moreConfident(AllData)
    #py.show()



################### CONTROL #################
if __name__ == "__main__":
  arguments = sys.argv
  answerFile = arguments[1]
  showDataControl(answerFile, 0)
  
