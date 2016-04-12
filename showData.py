# show survey data

import loadSurveyData as lSD
import sys
import pylab as py
import numpy as np
from scipy import stats
import math
import itertools as it



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
  


def plotQuestionHist(AllData, opsort):
  """
  organize question data into histogram; plot it and return it
  plot as pos (correct) and neg (incorrect) in same histogram 
  """
  corr = []
  incorr = []
  
  for i in AllData.keys():
    corr.append(AllData[i]['correct'].count(1))
    incorr.append(-(AllData[i]['correct'].count(0)))
  
  ary = np.array([corr, incorr])
  
  if opsort == 1:
    correct, incorrect = sortAndReturn(corr, incorr, 1)
    """
    new_ary = [(i, j) for i, j in zip(ary[0,:],ary[1,:])]
    new_ary.sort(key=lambda x : x[0], reverse=True)  # reverses order of list
    correct = []
    incorrect = []
    for i in range(len(new_ary)):
      correct.append(new_ary[i][0])
      incorrect.append(new_ary[i][1])
    """
    #incorrect = [i-2*i for i in incorrect]
   # print(correct)
   # print(incorrect)
  fig = py.figure()
  ax6 = fig.add_subplot(111)
  ax6.bar(range(len(correct)), correct, color='blue', edgecolor='white')
  ax6.bar(range(len(incorrect)), incorrect, color='red', edgecolor='white')
  
  ax6.set_ylabel('Correct')
  ax6.set_xlabel('Question No.')
  py.show()
  
  return correct, incorrect



def groupConfidenceVsCorrect(AllData):
  """
  plot and return % correct as a function of confidence
  redundant if hardest is called
  """
  
  avg_conf = []
  avg_correct = []
  for i in AllData.keys():
    avg_conf.append(np.mean(AllData[i]['confidence']))
    avg_correct.append(np.mean(AllData[i]['correct']))
    conf, correct = sortAndReturn(avg_conf, avg_correct, 1)
  
  #dens, bins, patches = py.hist(conf, 10, color='r', alpha=0.4,
  #                              linewidth=0, label='flash')
  py.bar(conf, correct, color='blue', linewidth=0, width=0.15, alpha=0.9)
  
  slope, intercept, r_value, p_value, std_err = stats.linregress(conf, correct)
  x1 = np.linspace(min(conf), max(conf),10)
  y1 = slope*x1 + intercept
  py.plot(x1,y1, 'r-', linewidth=0.5, label='flash')
  py.ylabel('Avg % correct')
  py.xlabel('Avg confidence')
  #py.show()
  
  print('R^2 is %.5f , P is %.5f ' % (r_value**2, p_value))
  
  return conf, correct



def indConfidenceVsCorrect(AllData, AllInfo):
  """
  plot and return individual confidences
  """
  copts = [1,2,3,4,5]
  fig = py.figure()
  print(AllInfo.keys())
  for i in AllInfo.keys():
    
    conf, corr = [], []
    
    for j in AllData.keys():
      conf.append(AllData[j]['confidence'][i-1])
      corr.append(AllData[j]['correct'][i-1])

    inds1 = [i for i, x in enumerate(conf) if x == 1]
    inds2 = [i for i, x in enumerate(conf) if x == 2]
    inds3 = [i for i, x in enumerate(conf) if x == 3]
    inds4 = [i for i, x in enumerate(conf) if x == 4]
    inds5 = [i for i, x in enumerate(conf) if x == 5]

    mean1 = [corr[i] for i in inds1]
    mean2 = [corr[i] for i in inds2]
    mean3 = [corr[i] for i in inds3]
    mean4 = [corr[i] for i in inds4]
    mean5 = [corr[i] for i in inds5]
    means = [np.mean(mean1), np.mean(mean2), np.mean(mean3), 
             np.mean(mean4), np.mean(mean5)]
    #print(means)
    ax3 = fig.add_subplot(111)
    ax3.plot(range(1,6), means, 'bo', alpha=0.4, linewidth=2)
    print(means)
  ax3.set_ylabel('% Correct')
  ax3.set_xlabel('Confidence')
  ax3.set_title('All responses')
  ax3.set_xticks(np.arange(1,6))
  ax3.set_xticklabels( [1, 2, 3, 4, 5] )
  ax3.set_xlim(0,6)
  ax3.set_ylim(-0.2,1.2)

  # py.show()
  
  


def hardest(AllData):
  """
  plot and return the 5 hardest questions
  """
  conf, correct = groupConfidenceVsCorrect(AllData)
  # take 5 hardest Qs
  corr2, conf2 = sortAndReturn(correct, conf, 0)
  meanconf = [np.mean(AllData[i]['confidence']) for i in AllData.keys()]
  stdconf = [np.std(AllData[i]['confidence']) for i in AllData.keys()]
  meancorr = [np.mean(AllData[i]['correct']) for i in AllData.keys()]
  stdcorr = [np.std(AllData[i]['correct']) for i in AllData.keys()]
  
  corr2 = trunc(corr2)
  conf2 = trunc(conf2)
  meanconf = trunc(meanconf)
  stdconf = trunc(stdconf)
  meancorr = trunc(meancorr)
  stdcorr = trunc(stdcorr)

  Qinds = []
  corr3=meancorr[:]
  for i in range(5):
    Qinds.append(corr3.index(corr2[i]))
    corr3[Qinds[-1]] = 5
    
  plotcorrs = [meancorr[i] for i in Qinds]
  plotcorrsstd = [stdcorr[i] for i in Qinds]
  plotconfs = [meanconf[i] for i in Qinds]
  plotconfsstd = [stdconf[i] for i in Qinds]
  
  width = 0.35
  prange = [float(i) for i in range(5)]
  prange2 = [prange[i] + width for i in range(5)]
  # plot
  #print(Qinds)
  
  fig = py.figure()
  ax = fig.add_subplot(111)
  rects1 = ax.bar(prange, plotcorrs, width, color='b', yerr=plotcorrsstd)
  ax2 = ax.twinx()
  rects2 = ax2.bar(prange2, plotconfs, width, color='r', yerr=plotconfsstd)
  ax.legend( (rects1[0], rects2[0]), ('% Correct', 'Confidence') )
  
  #rects1 = ax.bar(prange, plotcorrs, width, color='b', yerr=plotcorrsstd)
  #rects2 = ax.bar(prange2, plotconfs, width, color='r', 
  #                yerr = plotconfsstd)
  
  # plot specifics
  ax.set_ylabel('% Correct')
  ax2.set_ylabel('Confidence')
  ax.set_title('Hardest questions')
  ax.set_xticks(np.arange(5)+width)
  ax.set_xticklabels( [1, 2, 3, 4, 5] )
  ax.set_ylim(0, 1.3)
  ax2.set_ylim(0,6)
  return Qinds
  # py.show()
  



def doubleBars(group1, group2, std1=0, std2=0, plot_pars=None):
  width = 0.35
  prange = [float(i) for i in range(len(group1))]
  prange2 = [prange[i] + width for i in range(len(group1))]
  fig, ax = py.subplots()
  rects1 = ax.bar(prange, group1, width, color='b', yerr=std1)
  rects2 = ax.bar(prange2, group2, width, color='r', yerr = std2)
  
  if plot_pars:
  # plot specifics
    ax.set_ylabel(plot_pars['ylabel'])
    ax.set_title(plot_pars['title'])
    ax.set_xticks(np.arange()+width)
    ax.set_xticklabels(plot_pars['xticklabels'])
    ax.legend( (rects1[0], rects2[0]), plot_pars['legend'] )
    # legend is of format: ('% Correct', 'Confidence')
  # py.show()



def vsResponseTime(AllData):
  """
  plot confidence and % correct versus response time
  """
  avg_conf = []
  avg_correct = []
  avg_RT = []
  
  for i in AllData.keys():
    avg_conf.append(np.mean(AllData[i]['confidence']))
    avg_correct.append(np.mean(AllData[i]['correct']))
    avg_RT.append(np.mean(AllData[i]['RT']))
    
  RTcorr, correct = sortAndReturn(avg_RT, avg_correct, 1)
  RTconf, conf = sortAndReturn(avg_RT, avg_conf, 1)
  
  #dens, bins, patches = py.hist(conf, 10, color='r', alpha=0.4,
  #                              linewidth=0, label='flash')
  #py.bar(conf, correct, color='blue', linewidth=0, width=0.15, alpha=0.9)
  
  slope0, intercept0, r_value0, p_value0, std_err0 = stats.linregress(RTconf, correct)
  slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(RTcorr, conf)
  x0 = np.linspace(min(RTcorr), max(RTcorr),10)
  x1 = np.linspace(min(RTconf), max(RTconf),10)
  y0 = slope0*x0 + intercept0
  y1 = slope1*x0 + intercept1
  width = 0.35
  fig = py.figure()
  ax4 = fig.add_subplot(111)
  rects1 = ax4.plot(RTcorr, correct, 'bo')
  rects1 = ax4.plot(x0, y0, 'b', linewidth=4, alpha=0.4)
  ax5 = ax4.twinx()
  rects2 = ax5.plot(RTconf, conf, 'ro')
  rects2 = ax5.plot(x1, y1, 'r', linewidth=4, alpha=0.4)
  ax4.legend( (rects1[0], rects2[0]), ('% Correct', 'Confidence') )
  
  #rects1 = ax.bar(prange, plotcorrs, width, color='b', yerr=plotcorrsstd)
  #rects2 = ax.bar(prange2, plotconfs, width, color='r', 
  #                yerr = plotconfsstd)
  
  # plot specifics
  ax4.set_ylabel('% Correct')
  ax5.set_ylabel('Confidence')
  ax4.set_title('Response time ')
  #ax4.set_xticks(np.arange(5)+width)
  #ax4.set_xticklabels( [1, 2, 3, 4, 5] )
  ax4.set_ylim(0, 1.3)
  ax5.set_ylim(0,6)
  ax4.set_xlabel('Time (s)')
  
  # py.show()
  print('RT vs correct: R^2 is %.5f , P is %.5f ' 
        % (r_value0**2, p_value0))
  print('RT vs confidence: R^2 is %.5f, P is %.5f '
        % (r_value1**2, p_value1))
  
  return conf, correct
  


def racism(AllInfo):
  """
  sort data by language and gender, return the subjects in each
  group sorted by their index in AllInfo (which corresponds to the order
  in which their answers appear in AllData
  """
  possibleLangs = ['English', 'english', 'Chinese', 'chinese']
  possibleGens = ['Male', 'male', 'M', 'm', 'Female', 'female', 'F', 'f']
  gend = ['male', 'female']
  lang = ['english', 'chinese', 'euro']
  subjects = AllInfo.keys()
  maleSubjects = []
  femaleSubjects = []
  for i in AllInfo.keys():
    if AllInfo[i]['gend'] in possibleGens[0:4]:
      maleSubjects.append(i)
    elif AllInfo[i]['gend'] in possibleGens[4:]:
      femaleSubjects.append(i)
  english = []
  chinese = []
  euro = []
  for i in AllInfo.keys():
    if AllInfo[i]['lang'] in possibleLangs[0:2]:
      english.append(i)
    elif AllInfo[i]['lang'] in possibleLangs[2:]:
      chinese.append(i)
    else:
      euro.append(i)
  
  langs = {'english': english}
  langs['chinese'] = chinese
  langs['euro'] = euro
  gens = {'male': maleSubjects}
  gens['female'] = femaleSubjects
  
  return langs, gens



def plotByLanguage(AllData, AllInfo):
  """
  plot the data returned by 'racism'
  """
  colors = {'english': 'bo','chinese': 'ro', 'euro': 'ko'}
  color = {'english': 'b','chinese': 'r', 'euro': 'k'}
  langs, _ = racism(AllInfo)
  fig1 = py.figure()
  fig2 = py.figure()
  fig3 = py.figure()
  ax7 = fig1.add_subplot(111)
  ax8 = fig2.add_subplot(111)
  ax9 = fig3.add_subplot(111)
  # get each lang data
  for l in langs.keys():
    corrs, confs, RTs = [], [], []
    # get each question data
    print(langs[l])
    for j in AllData.keys():
      #print(j)
      # get each individual's data
      currentCorr, currentConf, currentRT = [], [], []
      for i in langs[l]:
        try:
          #print(i)
          #print('correct i %d and j %d' % (i, j))
          currentCorr.append(AllData[j]['correct'][i])
          #print('conf %d' %(AllData[j]['confidence'][i]))
          currentConf.append(AllData[j]['confidence'][i])
          #print('RT %d' %(AllData[j]['RT'][i]))
          currentRT.append(AllData[j]['RT'][i])
        except:
          pass
      corrs.append(np.mean(currentCorr))
      confs.append(np.mean(currentConf))
      RTs.append(np.mean(currentRT))
    
    # for each lang, plot stuff

    dots1 = ax7.plot(range(1,21), corrs, colors[l], alpha=1)
    ax7.plot(range(1,21), corrs, color[l], linewidth=3, alpha=0.2)
    dots2 = ax8.plot(range(1,21), confs, colors[l], alpha=1)
    ax8.plot(range(1,21), confs, color[l], linewidth=3, alpha=0.2)
    dots3 = ax9.plot(range(1,21), RTs, colors[l], alpha=1)
    ax9.plot(range(1,21), RTs, color[l], linewidth=3, alpha=0.2)
    ax7.set_ylim(-0.2,1.2)
    ax8.set_ylim(0,6)
    ax7.set_title('Language: Correct')
    ax8.set_title('Language: Confidence')
    ax9.set_title('Language: Response Time')
   # ax7.legend( ([0], rects2[0]), ('% Correct', 'Confidence') )
  



def plotByGenger(AllData, AllInfo):
  """
  plots same as language but by gender instead
  """
  colors = {'male': 'bo','female': 'ro'}
  color = {'male': 'b','female': 'r'}
  _ , gens = racism(AllInfo)
  fig1 = py.figure()
  fig2 = py.figure()
  fig3 = py.figure()
  ax7 = fig1.add_subplot(111)
  ax8 = fig2.add_subplot(111)
  ax9 = fig3.add_subplot(111)
  means = []
  # get each lang data
  for l in gens.keys():
    corrs, confs, RTs = [], [], []
    # get each question data
    print(gens[l])
    for j in AllData.keys():
      #print(j)
      # get each individual's data
      currentCorr, currentConf, currentRT = [], [], []
      for i in gens[l]:
        try:
          #print(i)
          #print('correct i %d and j %d' % (i, j))
          currentCorr.append(AllData[j]['correct'][i])
          #print('conf %d' %(AllData[j]['confidence'][i]))
          currentConf.append(AllData[j]['confidence'][i])
          #print('RT %d' %(AllData[j]['RT'][i]))
          currentRT.append(AllData[j]['RT'][i])
        except:
          pass
      corrs.append(np.mean(currentCorr))
      confs.append(np.mean(currentConf))
      RTs.append(np.mean(currentRT))
    means.append(np.mean(corrs))
    means.append(np.mean(confs))
    means.append(np.mean(RTs))
    
    # for each lang, plot stuff
    dots1 = ax7.plot(range(1,21), corrs, colors[l], alpha=1)
    ax7.plot(range(1,21), corrs, color[l], linewidth=3, alpha=0.2)
    dots2 = ax8.plot(range(1,21), confs, colors[l], alpha=1)
    ax8.plot(range(1,21), confs, color[l], linewidth=3, alpha=0.2)
    dots3 = ax9.plot(range(1,21), RTs, colors[l], alpha=1)
    ax9.plot(range(1,21), RTs, color[l], linewidth=3, alpha=0.2)
    ax7.set_ylim(-0.2,1.2)
    ax8.set_ylim(0,6)
    ax7.set_title('M vs F: Correct')
    ax8.set_title('M vs F: Confidence')
    ax9.set_title('M vs F: Response Time')
  print('Males percent corr: %.3f , mean conf: %.3f , mean RT: %.3f '
        % (means[0], means[1], means[2]))
  print('Females percent corr: %.3f , mean conf: %.3f , mean RT: %.3f '
        % (means[3], means[4], means[5]))



def getGroupSize(prange, mem):
  # return permutations of groups of size mem from subjects in prange
  perms = py.unique(list(it.combinations(prange, mem)))
  
  return perms



def getIndMeans(AllData, subject):
  """ 
  return the mean corrs, confs and RTs for a specific subject
  if subject == len(AllData[1]['correct']):
    subject = subject
  elif subject == len(AllData[1]['correct']) + 1:
    print('WARNING: subject %d not found in AllInfo' % subject )
  """
  corrs, confs, RTs = [], [], []
  for i in AllData.keys():
    corrs.append(AllData[i]['correct'][subject])
    confs.append(AllData[i]['confidence'][subject])
    RTs.append(AllData[i]['RT'][subject])

  means = [np.mean(corrs), np.mean(confs), np.mean(RTs)]
  return means



def getIndData(AllData, subject):
  # return the list of questions correct 1 or 0 for each question
  correct, conf, RTs = [], [], []
  for i in AllData.keys():
    correct.append(AllData[i]['correct'][subject])
    conf.append(AllData[i]['confidence'][subject])
    RTs.append(AllData[i]['RT'][subject])
  return correct, conf, RTs



def groupPercentCorrect(AllData, subjects, subset):
  # returns % correct for any number of subjects (=[list])
 # modes = dict.fromkeys(subjects)
  #print((subjects))
  #matrix = py.zeros([len(AllData.keys()), len(subjects)])
  matrix = py.zeros([len(AllData.keys()),len(subjects)])

  kcount = -1

  for k in AllData.keys():
    kcount += 1
    icount = 0
    while icount < len(subjects):
      matrix[kcount][icount] = \
                               AllData[k]['correct'][icount]
      icount += 1
  
  means = []
  for i in range(len(matrix[:][1])):
    current = []
    for j in subset:
      current.append(matrix[i][j])
    means.append( int(stats.mode(current)[0]) )
  
  meanmean = np.mean(means)
  #print matrix
  #print meanmean
  return meanmean

  """
  for k in AllData.keys():
    for i in modes.keys():
      modes[i] = []
      modes[i].append(AllData[k]['correct'][i])
  
  correct = []
  for j in modes.keys():
    newmodes = []
    for i in range(len(modes[j])):
      newmodes.append(modes[j][i])
    correct.append( int(stats.mode(newmodes)[0]) )
  print(np.mean(correct))
  return np.mean(correct)
  """
  
  



def plotGroupSize(AllData):
  """
  run permutations based on group size
  """
  means = []
  subjects = range(len(AllData[1]['correct']))
  
  for i in subjects[1:]:
    print(subjects[1:])
    current_means = []
    perms = py.unique(list(it.combinations(subjects, i)))

    for j in range(len(perms)):
      #print(len(perms[j]))
      current = groupPercentCorrect(AllData, subjects, perms[j])
      
      current_means.append(current)
    group_mean = np.mean(current_means)
    means.append(group_mean)
  
  #print(means)
  fig = py.figure()
  ax10 = fig.add_subplot(111)
  ax10.plot(subjects[1:], means, 'bo', alpha=1)
  ax10.plot(subjects[1:], means, 'b', linewidth=3, alpha=0.2)
  ax10.set_ylim(-0.2,1.2)
  ax10.set_title('Group Size: Percent Correct')
  
  # check means of all members individually
  submeans = []
  for i in subjects:
    curmean = getIndMeans(AllData, subjects[i])
    submeans.append(curmean[0])
  
  print('Individual means: %.3f ' % np.mean(submeans))
  



def getIndConf(AllData, subject, q = -1, plot = 0):
  """
  correct answers are multiplied by +C(1-5), incorrect are scaled 
  opposite (-1 - -5)
  """
  if q < 0:
    # get avg for all questions
    qnum = 20
    dist = []
    correct, confs, _ = getIndData(AllData, subject)
    print(len(correct), len(confs))
    i = 0
    while i < qnum:
      if correct[i] == 0:
        if confs[i] > 3:
          dist.append((confs[i]-2)*-0.1)
        elif confs[i] < 3:
          dist.append((confs[i])*0.1)
        else:
          dist.append(0)
      elif correct[i] == 1:
        if confs[i] > 3:
          dist.append(1+(confs[i]-2)*-0.1)
        elif confs[i] < 3:
          dist.append(1+(confs[i])*0.1)
        else:
          dist.append(1)
          #print('i = %d' %i)
      i += 1
    #print(correct, confs, dist)
    if plot==1:
      fig = py.figure()
      ax12 = fig.add_subplot(111)
      ax12.hist(dist, bins=10, color='b')
      ax12.set_title('Distribution of responses and confidence')
      ax12.set_ylabel('Count')
      ax12.set_xlabel('Correct')
      
    print(len(dist))
    return dist



def groupConfidenceWeight(AllData):
  """
  weights answers by confidence for different groups
  """
  # everybodygetup
  subjects = range(len(AllData[1]['correct']))
  
  distribution = np.array(py.zeros([20,len(subjects)]))
  for i in subjects:
    newdist = getIndConf(AllData, i)
    print(len(newdist))
    distribution[:,i] = newdist
  m,n = py.shape(distribution)
  for i in xrange(m):
    for j in xrange(n):
      distribution[i,j] = distribution[i,j] + py.randn(1)*0.05
  
  print(distribution)
  
  fig = py.figure()
  ax20 = fig.add_subplot(111)
  for i in xrange(n):
    ax20.hist(distribution[:,i], bins=20, color='c', alpha=0.2,
              edgecolor='none')
  ax20.set_title('Weighted answers')
  ax20.set_xlabel('Distribution')
  ax20.set_ylabel('Counts')
  



def genRandMatrix(AllData, subjects = -1):
  # create a random correct/incorrect matrix for questions and subjects
  if subjects < 0:
    # use the subjects from AllData as default
    subjects = range(len(AllData[2]['correct']))
  else:
    subjects = range(subjects)
    # else, use the number of subjects given
  numQs = len(AllData.keys())
  
  disto = py.rand(numQs, len(subjects))
  for i in range(numQs):
    for j in range(len(subjects)):
      if disto[i][j] > 0.4:
        disto[i][j] = 1
      else:
        disto[i][j] = 0
  #print(py.shape(disto))
  return disto




def randDist(AllData):
  # generate a group-size histo based on random data
  subjects = range(15)
  matrix = genRandMatrix(AllData, 15)
  #range(len(AllData[1]['correct']))
  
  meanmean = []
  for i in subjects[1:]:
    # create combination list
    #print(subjects[1:])
    
    perms = py.unique(list(it.combinations(subjects, i)))

    for h in range(len(perms)):
      # for each combination, get the mean correct
      means = []
      # print(len(matrix[:][1]))
      
      # change k for number of simulated questions
      k = 0
      while k < 20:
        #print(k)
        # for each question...
        current = []
        for j in perms[h]:
          #print(perms[h])
          # get the correct for that subject, append
          current.append(matrix[k][j])
        # then take the mode
        #print(int(stats.mode(current)[0]))
        means.append( int(stats.mode(current)[0]) )
        k += 1
      #print(means)
    # append mean for each group size

    meanmean.append(np.mean(means))
  allsum = sum(sum(matrix))
  m, n = py.shape(matrix)
  print('Total mean is %.3f / %.3f = %.3f '
        % ( allsum, m*n, (allsum/(m*n))))
  #print('subjects length %d , meanmean length %d ', 
         # % (len(subjects), len(meanmean)))
  subjects = subjects[1::2]
  meanmean = meanmean[1::2]
  fig = py.figure()
  ax13 = fig.add_subplot(111)
  ax13.plot(subjects, meanmean, 'bo', alpha=1)
  ax13.plot(subjects, meanmean, 'b', linewidth=3, alpha=0.2)
  ax13.set_ylim(-0.2,1.2)
  ax13.set_title('Random Group Size: Percent Correct')
  ax13.set_xlabel('Group size')
  ax13.set_ylabel('% Correct')
  print(meanmean)
  return meanmean
  



def AllDataDist(AllData):
  # 
  subjects = range(len(AllData[1]['correct']))
  matrix = py.zeros([len(AllData.keys()),len(subjects)])
  
  kcount = -1
  for k in AllData.keys():
    kcount += 1
    icount = 0
    while icount < len(subjects):
      matrix[kcount][icount] = \
                               AllData[k]['correct'][icount]
      icount += 1
  
  meanmean = []
  for i in subjects[1:]:
    # create combination list
    #print(subjects[1:])
    
    perms = py.unique(list(it.combinations(subjects, i)))

    for h in range(len(perms)):
      # for each combination, get the mean correct
      means = []
      for k in range(len(matrix[:][1])):
        # for each question...
        current = []
        for j in perms[h]:
          #print(perms[h])
          # get the correct for that subject, append
          current.append(matrix[k][j])
        # then take the mode
        #print(int(stats.mode(current)[0]))
        means.append( int(stats.mode(current)[0]) )
      #print(means)
    # append mean for each group size

    meanmean.append(np.mean(means))
  allsum = sum(sum(matrix))
  m, n = py.shape(matrix)
  print('Total mean is %.3f / %.3f = %.3f '
        % ( allsum, m*n, (allsum/(m*n))))
  
  subjects = subjects[1::2]
  meanmean = meanmean[1::2]
  if len(subjects) > len(meanmean):
    subjects=subjects[1:]
  elif len(subjects) < len(meanmean):
    meanmean = meanmean[1:]
  fig = py.figure()
  ax14 = fig.add_subplot(111)
  ax14.plot(subjects, meanmean, 'bo', alpha=1)
  ax14.plot(subjects, meanmean, 'b', linewidth=3, alpha=0.2)
  ax14.set_ylim(-0.2,1.2)
  ax14.set_title('Real Data Group Size: Percent Correct')
  ax14.set_xlabel('Group size')
  ax14.set_ylabel('% Correct')
  print(meanmean)
  return meanmean




def returnConfMatrix(AllData):
  # returns the confidence matrix
  subjects = range(len(AllData[1]['correct']))
  correctmatrix = py.zeros([len(AllData.keys()),len(subjects)])
  confmatrix = py.zeros([len(AllData.keys()),len(subjects)])

  kcount = -1
  for k in AllData.keys():
    kcount += 1
    icount = 0
    while icount < len(subjects):
      correctmatrix[kcount][icount] = \
                               AllData[k]['correct'][icount]
      icount += 1
  kcount = -1
  for k in AllData.keys():
    kcount += 1
    icount = 0
    while icount < len(subjects):
      confmatrix[kcount][icount] = \
                               AllData[k]['confidence'][icount]
      icount += 1

  return correctmatrix, confmatrix
  




def correctBias(AllData):
  # correct for difficulty and plot each subject %correct vs confidence
  corrmatrix, confmatrix = returnConfMatrix(AllData)
  Qs, subjects = py.shape(corrmatrix)
  copts = [1,2,3,4,5]
  datamat = np.array(py.zeros([len(copts), subjects]))
  print(datamat)
  fig = py.figure()
  ax15 = fig.add_subplot(111) 
  i = 0
 
  while i < subjects:
    c1, c2, c3, c4, c5 = [],[],[],[],[]
    # get confidences for each subject
    j = 0
    while j < Qs:
      # get confidences and correct for each question
      if confmatrix[j][i] == 1:
        c1.append(corrmatrix[j][i])
      elif confmatrix[j][i] == 2:
        c2.append(corrmatrix[j][i])
      elif confmatrix[j][i] == 3:
        c3.append(corrmatrix[j][i])
      elif confmatrix[j][i] == 4:
        c4.append(corrmatrix[j][i])
      elif confmatrix[j][i] == 5:
        c5.append(corrmatrix[j][i])
      else:
        print('bad num encountered')
        
      j += 1
    print('i is %d' %i)
    minconf = ([py.mean(c1), py.mean(c2), py.mean(c3), 
                   py.mean(c4), py.mean(c5)])
    pmin = 10
    for p in minconf:
      if p < pmin and p != 0 and math.isnan(p) is not True:
        pmin = p
    
    print(pmin)
    datamat[0][i] = py.mean(c1)/pmin
    datamat[1][i] = py.mean(c2)/pmin
    datamat[2][i] = py.mean(c3)/pmin
    datamat[3][i] = py.mean(c4)/pmin
    datamat[4][i] = py.mean(c5)/pmin
    # print(datamat)
    print( py.shape(datamat))
    print(len(datamat[:,i]))
    ax15.plot(range(1,6), datamat[:,i], alpha=0.4, linewidth=4)
    i += 1
  
  ax15.set_ylabel('Modified Correct')
  ax15.set_xlabel('Confidence')
  ax15.set_title('All responses')
  ax15.set_xticks(np.arange(1,6))
  ax15.set_xticklabels( [1, 2, 3, 4, 5] )
  ax15.set_xlim(0,6)
  #ax14.set_ylim(-0.2,1.2)
  



def confidenceLevels(AllData):
  # separate groups into high/low confidence and plot answers
  # correctmatrix, confmatrix = returnConfMatrix(AllData)
  
  corrs, confs, RTs = [], [], [] 
  for s in range(len(AllData[1]['correct'])):
    current_corr, current_conf, current_RTs = getIndMeans(AllData, s)
    corrs.append(current_corr)
    confs.append(current_conf)
    RTs.append(current_RTs)
    
  # do confidences
  conf_t = py.median(confs)
  low_conf, high_conf = [], []
  for i in range(len(confs)):
    if confs[i] > conf_t:
      high_conf.append(i)
    else:
      low_conf.append(i)
  high_conf_corr, low_conf_corr = [], []
  high_conf_corr = [corrs[i] for i in high_conf]
  low_conf_corr = [corrs[i] for i in low_conf]
  HCmeancorr, HCstdcorr = py.mean(high_conf_corr), py.std(high_conf_corr)
  LCmeancorr, LCstdcorr = py.mean(low_conf_corr), py.std(low_conf_corr)
  HC_RT = [RTs[i] for i in high_conf]
  LC_RT = [RTs[i] for i in low_conf]
  HC_RT_mean, HC_RT_std = py.mean(HC_RT), py.std(HC_RT)
  LC_RT_mean, LC_RT_std = py.mean(LC_RT), py.std(LC_RT)
  corrmean = [HCmeancorr, LCmeancorr]
  corrstd = [HCstdcorr, LCstdcorr]
  RTmean = [HC_RT_mean, LC_RT_mean]
  RTstd = [HC_RT_std, LC_RT_std]
  
  # plot
  width = 0.35
  fig = py.figure()
  ax16 = fig.add_subplot(111)
  rects1 = ax16.bar([1,2], corrmean, width, color='b', yerr=corrstd)
  ax17 = ax16.twinx()
  rects2 = ax17.bar([1.5,2.5], RTmean, width, color='r', yerr = RTstd)
  plot_pars = {'ylabel': '% correct', 'title': 'High vs Low Confidence',
               'xticklabels': ['High', 'Low'], 'legend': ['% Correct', 'RT']}
  ax16.set_ylabel(plot_pars['ylabel'])
  ax16.set_title(plot_pars['title'])
  ax16.set_xticks([1.25, 2.25])
  ax16.set_xticklabels(plot_pars['xticklabels'])
  ax16.legend( (rects1[0], rects2[0]), plot_pars['legend'] )
  
  corrs, confs, RTs = [], [], [] 
  for s in range(len(AllData[1]['correct'])):
    current_corr, current_conf, current_RTs = getIndMeans(AllData, s)
    corrs.append(current_corr)
    confs.append(current_conf)
    RTs.append(current_RTs)
    
  ### now do reaction times
  RT_t = py.median(RTs)
  low_RT, high_RT = [], []
  for i in range(len(RTs)):
    if RTs[i] > RT_t:
      high_RT.append(i)
    else:
      low_RT.append(i)
  high_RT_corr, low_RT_corr = [], []
  high_RT_corr = [corrs[i] for i in high_RT]
  low_RT_corr = [corrs[i] for i in low_RT]
  HRTmeancorr, HRTstdcorr = py.mean(high_RT_corr), py.std(high_RT_corr)
  LRTmeancorr, LRTstdcorr = py.mean(low_RT_corr), py.std(low_RT_corr)
  HRT_conf = [confs[i] for i in high_RT]
  LRT_conf = [confs[i] for i in low_RT]
  HRT_conf_mean, HRT_conf_std = py.mean(HRT_conf), py.std(HRT_conf)
  LRT_conf_mean, LRT_conf_std = py.mean(LRT_conf), py.std(LRT_conf)
  corrmean = [HRTmeancorr, LRTmeancorr]
  corrstd = [HRTstdcorr, LRTstdcorr]
  confsmean = [HRT_conf_mean, LRT_conf_mean]
  confstd = [HRT_conf_std, LRT_conf_std]
  
  # plot
  width = 0.35
  fig = py.figure()
  ax18 = fig.add_subplot(111)
  rects1 = ax18.bar([1,2], corrmean, width, color='b', yerr=corrstd)
  ax19 = ax18.twinx()
  rects2 = ax19.bar([1.5,2.5], confsmean, width, color='r', yerr = confstd)
  plot_pars = {'ylabel': '% correct', 'title': 'High vs Low RT',
               'xticklabels': ['High', 'Low'], 'legend': ['% Correct', 'Conf']}
  ax18.set_ylabel(plot_pars['ylabel'])
  ax18.set_title(plot_pars['title'])
  ax18.set_xticks([1.25, 2.25])
  ax18.set_xticklabels(plot_pars['xticklabels'])
  ax18.legend( (rects1[0], rects2[0]), plot_pars['legend'] )
  
 # print(high_conf_corr)
    






def showDataControl(answerFile, version=1):
  """
  run the plotting functions and display the data
  """
  # load answer data from lSD program
  #print('control called')
  AllData, AllInfo = lSD.answerControl(answerFile, 0)
  print AllData
  
  if version==1:
    correct, incorrect = plotQuestionHist(AllData, 1)
    groupConf, groupCorrect = groupConfidenceVsCorrect(AllData)
    Qinds = hardest(AllData)
    print(Qinds)
    indConfidenceVsCorrect(AllData, AllInfo)
    vsResponseTime(AllData)
    plotByLanguage(AllData, AllInfo)
    plotByGenger(AllData, AllInfo)
    plotGroupSize(AllData)
    randDist(AllData)
    AllDataDist(AllData)
    correctBias(AllData)
    confidenceLevels(AllData)
    groupConfidenceWeight(AllData)
    py.show()
  
  elif version==0:
    


    py.show()



################### CONTROL #################
if __name__ == "__main__":
  arguments = sys.argv
  answerFile = arguments[1]
  showDataControl(answerFile, 1)
  
