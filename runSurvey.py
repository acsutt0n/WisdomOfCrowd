# runSurvey.py - 
# usage: [0]python [1]runSurvey.py [2]question_bank.txt [3]outFile.txt

import sys
from display_question import *
from datetime import datetime
from datetime import timedelta



def readLine(line, Current):
  """
  Read each line and parse for questions.
  """
  # print('readLine called')
  
  splitLine = line.split(None)
  if not splitLine:
    print('blank line found')
  
  # try to read each line of the file
  try:
    i = int(splitLine[0].split('.')[0])
  except:
    i = -1

  # questions start with hashes, reset dictionary
  if splitLine[0] == '#':
    print('found hash')
    Current = {'openQuestion': 1}
    Current['readQuestion'] = 0
    Current['closeQuestion'] = 0
  
  # else, if the question is open and an int is in col[0]
  elif Current['openQuestion']==1 and i > 0:
    print('Q number found')
    Current['questionNum'] = i
    Current['readQuestion'] = 1
  
  # read the next line as a question
  elif Current['openQuestion']==1 and Current['readQuestion']==1:
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
    print('found weight')
    Current['weight'] = splitLine[1]
    Current['openQuestion'] = 0
    Current['closeQuestion'] = 1
  
  else:
    print('blank space found')
  
  return Current
    


def loadQuestions(questionFile):
  """
  Load questions.
  """
  Current ={0:0} # set dict to empty for start

  print(questionFile)
  lineNum = 0
  with open(questionFile, 'r') as infile:
    try:
      
      for line in infile:

        lineNum = lineNum + 1
        Current = readLine(line, Current)
        
        # if the section has been closed, read the Current info
        # into the question bank dictionary

        if Current['closeQuestion']:
          if Current['closeQuestion'] == 1:
            print(Current)
            if Current['questionNum'] == 1:
              Question = {Current['questionNum']: Current}
              print('created Question dict')
            else:
              print(Current['questionNum'])
              Question[Current['questionNum']] = Current
              print('added question item')

    except:
      print('Error reading line %d' % lineNum)
    
  print(Question.keys())
  if len(Question.keys()) > 10:
    return Question
  else:
    print('Question is only %i' %len(Question))
    





def prepQuestions(questionFile):
  """
  Load up question dictionary; call only once
  """
  try:
    Question = loadQuestions(questionFile)
  except:
    print('Error loading question file %s' % questionFile)
#  print(Question)
  #print(len(Q
  if len(Question.keys()) < 20:
    print('Error loading question file')
  else:
    return Question
  


def getInfo():
  """
  Get relevant info before beginning trial. Call only once per subject
  """
  name = raw_input('First (given) and last (surname) name: ')
  cont = raw_input('Continent where you were born: ')
  gend = raw_input('Gender: ')
  
  Info = {'name': name, 'cont': cont, 'gend': gend}



def initAnswers():
  """
  Initialize the answer dictionary
  """
  Answers = {0: 1}
  return Answers



def askQuestion(Question, questionNum, Answers):
  """
  When called, this method poses the desired question to the user
  and returns the answer and response time. Confidence should be called
  next.
  """
  if not Answers:
    Answers = initAnswers()
  
  print(Question[questionNum])
  current_line = Question[questionNum]['questionLine']
  print('Question # %i: ' %questionNum)
  print(current_line)
  cA = Question[questionNum]['choiceA']
  cB = Question[questionNum]['choiceB']
  print(cA)
  print(cB)
  start = datetime.now()
  ans = raw_input('Answer: ')
  stop = datetime.now()
  RT = (stop - start)
  
  if ans=='a' or ans=='A' or ans==1:
    ans = 'A'
  elif ans=='b' or ans=='B' or ans==2:
    ans = 'B'
  else:
    print('Bad answer given for question %i' %questionNum)
  # log answer as correct (=1) or incorrect
  if Question[questionNum]['answer'] == ans:
    currentAnswer = {'correct': 1}
  else:
    currentAnswer = {'correct': 0}
  
  # log response time
  currentAnswer['RT'] = RT
    
  Answers[questionNum] = currentAnswer
  return Answers



def getConfidence(questionNum, Answers):
  """
  Ask the user to input their confidence on a scale of 1-5. Called 
  after every question.
  """
  print('How confident are you that your answer was correct?')
  conf = raw_input('(Scale of 1 (least confident) - - - - 5 (very confident):')
  try:
    conf = int(conf)
  except:
    print('Non-intergerable value entered for question %i' %questionNum)
  
  if conf > 5:
    conf = 5
  elif conf < 1:
    conf = 1
  
  Answers[questionNum]['conf'] = conf
  return Answers
  


def compileAnswers(Answers, outFile):
  """
  Write the answers from the Answers dict to the given file.
  """
  if outFile is None:
    outFile = 'new_results.txt'
    
  f = open(outFile, 'w')
  numQs = max(Answers.keys())
  
  # write each dict element to file
  for l in range(1, numQs):
    print(Answers[l])
    ansLine = Answers[l]
    # write each element in each dict item to line
    for item in ansLine.values():
      f.write('%s ' %item)
    f.write('\n') # create new line
  
  f.close()
  print('File %s written.' %outFile)
  


def control(questionFile, outFile):
  """
  Called just once per user, this steps through all the operations 
  necessary to run the survey:
    1. load questions: prepQuestions(questionFile)
    2. initialize answers: initAnswers()
    3. get user info: getInfo()
    4. Run through all questions:
       a. ask a question: askQuestion(Question, questionNum)
       b. get user's confidence: getConfidence(questionNum, Answers)
       c. advance to next question
    5. compile answers and save as txt file that's easy to read
  """
  
  Question = prepQuestions(questionFile)
  print('Questions loaded.')
  Answers = initAnswers()
  Info = getInfo()
  print('User info loaded')
  
  # run through questions
  numQs = max(Question.keys())
  
  for q in xrange(1,21):
    
    # get answer to current question
    Answers = askQuestion(Question, q, Answers)
    # get confidence & add to answer
    Answers = getConfidence(q, Answers)
    
    print('%i / %i completed.' %(q, numQs))
  
  compileAnswers(Answers, outFile)
  print('Answers saved. Thanks!')
  
    
    
  
  
  






## CONTROL
"""

"""
if __name__ == "__main__":
  arguments = sys.argv
  # print(len(arguments))
  #
  questionFile = arguments[1]
  outFile = arguments[2]
  control(questionFile, outFile)
  






