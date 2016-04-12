## this program reads and displays the questions in question bank
# when it's called
# usage: python display_question.py questionFile(.txt)

import sys

def readLine(line, Current):
  splitLine = line.split(None)
  if not splitLine:
    return
  
  # try to read each line of the file
  try:
    i = int(splitLine[0].split('.')[0])
  except:
    i = -1
  
  # questions start with hashes, reset dictionary
  if splitLine[0] == '#':
    print('found hash')
    Current = dict
    Current = {'openQuestion': 1}
    Current['readQuestion'] = 0
    Current['closeQuestion'] = 0
  
  # else, if the question is open and an int is in col[0]
  elif Current['openQ']==1 and i > 0:
    Current['questionNum'] = i
    Current['readQuestion'] = 1
  
  # read the next line as a question
  elif Current['openQ']==1 and Current['readQuestion']==1:
    Current['questionLine'] = line
    Current['readQuestion'] = 0
  
  # read answer
  elif splitLine[0] == '&':
    Current['answer'] = splitLine[1]
  
  # read answer choices
  elif splitLine[0] == 'A.':
    Current['choiceA'] = line
  elif splitLine[0] == 'B.':
    Current['choiceB'] = line
  
  # read 'weight' and close current question
  elif splitLine[0] == '%':
    Current['weight'] = splitLine[1]
    Current['openQuestion'] = 0
    Current['closeQuestion'] = 1
  
  else:
    return
  
  return Current
    

def loadQuestions(questionFile):
  
  Current = dict # set dict to empty for start

  
  lineNum = 0
  with open(questionFile, 'r') as infile:
    try:
      for line in infile:
        
        lineNum += 1
        Current = readLine(line, Current)
        
        # if the section has been closed, read the Current info
        # into the question bank dictionary
        if Current['closeQuestion']==1:
          if not Question:
            Question = {Current['questionNum']: Current}
          else:
            Question[Current['questionNum']] = Current
            
        
    except:
      return
    
  return Question
    



















#############################################################
if __name__ == "__main__":
  # pass files and args to main function
  
  questionFile = sys.args[2]
  # questionNum = sys.args[3]
  Question = loadQuestions(questionFile)

