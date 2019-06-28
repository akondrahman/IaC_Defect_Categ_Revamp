'''
Akond Rahman 
April 12, 2019 
Mining metrics: Main 
'''

import pandas as pd 
import cPickle as pickle
import metric_miner 
import os 
import csv 
import time
import datetime

def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def getEligibleProjects(fileNameParam):
  repo_list = []
  with open(fileNameParam, 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
      repo_list.append(row[0])
  return repo_list
'''
This script goes to each repo and mines commits and get metrics for each commit 
'''
###  columns=['COMMIT_HASH', 'FILE_CNT', 'DIR_CNT', 'LOC_MODI' 'SPREAD', 'DEVS_FILE', 'DEVS_EXP', 'DEVS_REXP']

if __name__=='__main__': 
  metric_flag = False 
  t1 = time.time()
  print 'Started at:', giveTimeStamp()
  print '*'*100  

  # orgName='ghub-downloads'
  # out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/GHUB_METRICS_OUTPUT_FINAL.csv'
  # out_hash_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/GHUB_HASH_FILE_OUTPUT_FINAL.csv'

  # orgName     = 'mozilla-releng-downloads'
  # out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/MOZI_METRICS_OUTPUT_FINAL.csv'
  # out_hash_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/MOZI_HASH_FILE_OUTPUT_FINAL.csv'

  orgName='openstack-downloads'
  out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_METRICS_OUTPUT_FINAL.csv'
  out_hash_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_HASH_FILE_OUTPUT_FINAL.csv'  

  # orgName='wikimedia-downloads'
  # out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_METRICS_OUTPUT_FINAL.csv'
  # out_hash_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_HASH_FILE_OUTPUT_FINAL.csv'  

  fileName          = '/Users/akond/ICSE2020_PUPP_REPOS/'  + orgName + '/' + 'eligible_repos.csv' 
  elgibleRepos      = getEligibleProjects(fileName)
  metrics_all_proj  = [] 
  if metric_flag:
    for proj_ in elgibleRepos:
      metrics_as_list   = metric_miner.runMiner(orgName, proj_, 'master')    
      metrics_all_proj = metrics_all_proj + metrics_as_list 

    final_metric_df = pd.DataFrame(metrics_all_proj)
    print final_metric_df.head() 
    final_metric_df.to_csv(out_csv_fil, header=['HASH', 'MOD_FILES', 'DIRS', 'TOT_SLOC', 'SPREAD', 'DEV_CNT_MOD_FILES', 'DEV_EXP', 'DEV_REXP'], index=False)   
  else: 
    for proj_ in elgibleRepos:
      files_as_list     = metric_miner.getPuppFilesNHashes(orgName, proj_, 'master')    
      metrics_all_proj  = metrics_all_proj + files_as_list

    final_metric_df = pd.DataFrame(metrics_all_proj)
    print final_metric_df.head() 
    final_metric_df.to_csv(out_hash_file, header=['HASH', 'FILE'], index=False)     

  print '*'*100
  print 'Ended at:', giveTimeStamp()
  print '*'*100
  t2 = time.time()
  time_diff = round( (t2 - t1 ) / 60, 5) 
  print "Duration: {} minutes".format(time_diff)
  print '*'*100  