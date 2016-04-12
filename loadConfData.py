# load up the data, run some analyses
# usage: python loadSurveyData.py -options

import sys


def addInfo(CurrentInfo, AllInfo):
  """
  Collect all info into one dataset
  """
  if not AllInfo:
    AllInfo = {1: CurrentInfo}
  else:
    AllInfo[len(AllInfo.keys())+1] = CurrentInfo
  
  return AllInfo
  
def addData(CurrentData, AllData):
  """
  Collect all data into one dataset
  """
  #print('addData called')
  if not AllData:
    AllData = dict.fromkeys(CurrentData['questionNum'])
    for q in AllData.keys():
      AllData[q] = {'correct': []}
      AllData[q]['confA'] = []
      AllData[q]['confB'] = []
      AllData[q]['RT'] = []
  
  # questions range from 1-20
  for i in range(1,17):
    AllData[i]['correct'].append(CurrentData['correct'][i-1])
    AllData[i]['confA'].append(CurrentData['confA'][i-1])
    AllData[i]['confB'].append(CurrentData['confB'][i-1])
    AllData[i]['RT'].append(CurrentData['RT'][i-1])
  
  return AllData
  


def readAnswers(answerFile):
  """
  read each line and add to dict
  """
  """
  Load answers into dict for analysis
  """
  #print('readAnswers called')
  AllInfo, AllData = None, None
  CurrentInfo, CurrentData = None, None
  lineNum = 0
  
  with open(answerFile, 'r') as fIn:
   # try:
      
    for line in fIn:
      lineNum = lineNum + 1
     #  print(lineNum)
      splitLine = line.split(None)
      
      if not splitLine:
        print('bad line: %d' % lineNum)
      
      if splitLine[0] == 'lang:':
        # print('load info')
        
        # log previous subject data
        if CurrentInfo:
          AllInfo = addInfo(CurrentInfo, AllInfo)
        if CurrentData:
          AllData = addData(CurrentData, AllData)
          
        CurrentInfo = {'lang': splitLine[1]}
        CurrentInfo['gend'] = splitLine[3]
        CurrentInfo['name'] = splitLine[5]
        # reset current data
        CurrentData = {'questionNum': []}
        CurrentData['correct'] = []
        CurrentData['confA'] = []
        CurrentData['confB'] = []
        CurrentData['RT'] = []
      
      if len(splitLine) == 5:
        # print('load data')
        # Answers['currentQuestion'] = Answers['currentQuestion'] + 1
        CurrentData['confA'].append(float(splitLine[0]))
        if CurrentData['confA'][-1] > 10:
          CurrentData['confA'][-1] = CurrentData['confA'][-1] / 10
        RT = float(splitLine[1].split(':')[2])
        CurrentData['RT'].append(RT)
        CurrentData['questionNum'].append(int(splitLine[2]))
        CurrentData['correct'].append(int(splitLine[4]))
        CurrentData['confB'].append(float(splitLine[3]))
        if CurrentData['confB'][-1] > 10:
          CurrentData['confB'][-1] = CurrentData['confB'][-1] / 10
      
      else:
        pass
          
 #   except:
 #     print('E')
  
  return AllData, AllInfo




def answerControl(answerFile, printOption=1):
  """
  
  """
  print(printOption)
  AllData, AllInfo = readAnswers(answerFile)
  if printOption == True or printOption == 1:
    print(AllData)
    print(AllInfo)
  
  return AllData, AllInfo
  
  










########### CONTROL #############
"""
"""
if __name__ == "__main__":
  arguments = sys.argv
  answerFile = arguments[1]
  printOption = arguments[2]
  answerControl(answerFile, printOption)




