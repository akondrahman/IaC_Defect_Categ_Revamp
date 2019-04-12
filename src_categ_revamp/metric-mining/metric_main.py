'''
Akond Rahman 
April 12, 2019 
Mining metrics: Main 
'''

import pandas as pd 
import cPickle as pickle
import metric_miner 

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

if __name__=='__main__': 
    orgName='wikimedia-downloads'
    out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_METRICS_OUTPUT_FINAL.csv'
    out_pkl_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_METRICS_OUTPUT_FINAL.PKL'

    # orgName='openstack-downloads'
    # out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_METRICS_OUTPUT_FINAL.csv'
    # out_pkl_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_METRICS_OUTPUT_FINAL.PKL'    

    fileName     =  '/Users/akond/PUPP_REPOS/'  + orgName + '/' + 'eligible_repos.csv' 
    elgibleRepos =   getEligibleProjects(fileName)
    dic   = {}
    categ = [] 
    for proj_ in elgibleRepos:
        per_proj_commit_dict, per_proj_full_defect_list = metric_miner.runMiner(orgName, proj_, 'master')    