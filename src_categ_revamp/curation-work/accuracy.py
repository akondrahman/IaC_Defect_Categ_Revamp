'''
May 30, 2019
Thursday 
Akond Rahman
Script to detect accuracy of SLIC
'''

from sklearn.metrics import precision_score, recall_score
import numpy as np, pandas as pd
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def printAccu(file_name):
  df2read = pd.read_csv(file_name)
  actualLabels = df2read['ORACLE'].tolist()
  predictedLabels = df2read['TOOL'].tolist()
  # print actualLabels
  '''
    the way skelarn treats is the following: first index -> lower index -> 0 -> 0
                                             next index after first  -> next lower index -> 1 -> 1
  '''
  '''
  getting the confusion matrix
  '''
  print "Confusion matrix start"
  #print conf_matr_output
  conf_matr_output = confusion_matrix(actualLabels, predictedLabels)
  print conf_matr_output
  print "Confusion matrix end"
  print ">"*10
  '''
  '''
  print "precison, recall, F-stat"
  class_report = classification_report(actualLabels, predictedLabels)
  print class_report
  print ">"*10
  '''
  accuracy_score ... reff: http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter .... percentage of correct predictions
  ideally 1.0, higher the better
  '''
  accuracy_score_output = accuracy_score(actualLabels, predictedLabels)
  # preserve the order first test(real values from dataset), then predcited (from the classifier )
  # print "Accuracy output is ", accuracy_score_output
  # print">"*10


if __name__=='__main__':

  #  acid_ds = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/closed-coding-2019/LOCKED_FOR_PAPER_FINAL_CLASSI_OUTPUT_ORACLE.csv'
   acid_ds = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/closed-coding-2019/OR_ACCURACY_ORACLE.csv'
  
   printAccu(acid_ds)

  #  sanity_ds = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/sanity-check-2019/500_ACCURACY_SANITY_CHECK_OSTK.csv'
  # sanity_ds = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/sanity-check-2019/OR_500_ACCURACY_SANITY_CHECK_OTUPUT_OSTK.csv'

  # sanity_ds = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/sanity-check-2019/500_LOCKED_FOR_PAPER_SANITY_CHECK_RESULTS_WIKI.csv'
  # printAccu(sanity_ds)