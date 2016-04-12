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
  print('addData called')
  if not AllData:
    AllData = dict.fromkeys(CurrentData['questionNum'])
    for q in AllData.keys():
      AllData[q] = {'correct': []}
      AllData[q]['confidence'] = []
      AllData[q]['RT'] = []
  
  # questions range from 1-20
  for i in range(1,21):
    AllData[i]['correct'].append(CurrentData['correct'][i-1])
    AllData[i]['confidence'].append(CurrentData['confidence'][i-1])
    AllData[i]['RT'].append(CurrentData['RT'][i-1])
  
  return AllData
  


def readAnswers(answerFile):
  """
  read each line and add to dict
  """
  """
  Load answers into dict for analysis
  """
  
  AllInfo, AllData = None, None
  CurrentInfo, CurrentData = None, None
  lineNum = 0
  
  with open(answerFile, 'r') as fIn:
   # try:
      
    for line in fIn:
      lineNum = lineNum + 1
      print(lineNum)
      splitLine = line.split(None)
      
      if not splitLine:
        print('bad line?')
      
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
        CurrentData['confidence'] = []
        CurrentData['RT'] = []
      
      if len(splitLine) == 4:
        # print('load data')
        # Answers['currentQuestion'] = Answers['currentQuestion'] + 1
        RT = float(splitLine[0].split(':')[2])
        CurrentData['RT'].append(RT)
        CurrentData['questionNum'].append(int(splitLine[1]))
        CurrentData['correct'].append(int(splitLine[2]))
        CurrentData['confidence'].append(int(splitLine[3]))
      
      elif splitLine[0] == 'end':
        print('end of file')
        AllData = addData(CurrentData, AllData)
        AllInfo = addInfo(CurrentInfo, AllInfo)
    
 #   except:
 #     print('E')
  
  return AllData, AllInfo




def answerControl(answerFile, printOption):
  """
  
  """
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
  answerControl(answerFile, printOption=1)




