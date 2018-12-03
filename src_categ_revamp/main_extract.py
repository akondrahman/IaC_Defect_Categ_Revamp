'''
Akond Rahman 
Dec 02, 2018 
Revamping Defect Categ project : Extraction 
'''
import os 
import csv 
import numpy as np
import sys
from git import Repo
import  subprocess
import time 
import  datetime 

def getEligibleProjects(fileNameParam):
  repo_list = []
  with open(fileNameParam, 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
      repo_list.append(row[0])
  return repo_list

def getPuppetFilesOfRepo(repo_dir_absolute_path):
    pp_, non_pp = [], []
    for root_, dirs, files_ in os.walk(repo_dir_absolute_path):
       for file_ in files_:
           full_p_file = os.path.join(root_, file_)
           if((os.path.exists(full_p_file)) and ('EXTRA_AST' not in full_p_file) ):
             if (full_p_file.endswith('.pp')):
               pp_.append(full_p_file)
    return pp_


def getRelPathOfFiles(all_pp_param, repo_dir_absolute_path):
  common_path = repo_dir_absolute_path
  files_relative_paths = [os.path.relpath(path, common_path) for path in all_pp_param]
  return files_relative_paths 

def getPuppRelatedCommits(repo_dir_absolute_path, ppListinRepo, branchName='master'):
  mappedPuppetList=[]
  track_exec_cnt = 0
  repo_  = Repo(repo_dir_absolute_path)
  all_commits = list(repo_.iter_commits(branchName))
  for each_commit in all_commits:
    track_exec_cnt = track_exec_cnt + 1

    cmd_of_interrest1 = "cd  " + repo_dir_absolute_path + " ; "
    cmd_of_interrest2 = "git show --name-status " + str(each_commit)  +  "  | awk '/.pp/ {print $2}'"
    cmd_of_interrest = cmd_of_interrest1 + cmd_of_interrest2
    commit_of_interest  = subprocess.check_output(['bash','-c', cmd_of_interrest])

    for ppFile in ppListinRepo:
      if ppFile in commit_of_interest:

       file_with_path = os.path.join(repo_dir_absolute_path, ppFile)
       mapped_tuple = (file_with_path, each_commit)
       mappedPuppetList.append(mapped_tuple)

  return mappedPuppetList



def getPuppCommitFullData(repo_path_param, repo_branch_param, pupp_commits_mapping):
  trac_exec_count = 0 
  pupp_bug_list = []
  for tuple_ in pupp_commits_mapping:
    file_ = tuple_[0]
    commit_ = tuple_[1]
    msg_commit =  commit_.message 

    msg_commit = msg_commit.replace('\n', ' ')
    msg_commit = msg_commit.replace(',',  ';')    
    msg_commit = msg_commit.replace('\t', ' ')
    msg_commit = msg_commit.replace('&',  ';')  
    msg_commit = msg_commit.replace('#',  ' ')
    msg_commit = msg_commit.replace('=',  ' ')      


    timestamp_commit = commit_.committed_datetime
    str_time_commit  = timestamp_commit.strftime('%Y-%m-%dT%H-%M-%S')

    tup_ = (repo_path_param, trac_exec_count, file_, str_time_commit, msg_commit, repo_branch_param )
    pupp_bug_list.append(tup_)

    trac_exec_count += 1

  return pupp_bug_list

def constructDataset(orgParamName, repo_name_param, branchParam):

  repo_path   = "/Users/akond/PUPP_REPOS/" + orgParamName + "/" + repo_name_param
  repo_branch = branchParam

  all_pp_files_in_repo = getPuppetFilesOfRepo(repo_path)
  # print all_pp_files_in_repo
  
  rel_path_pp_files = getRelPathOfFiles(all_pp_files_in_repo, repo_path)
  # print rel_path_pp_files

  pupp_commits_in_repo = getPuppRelatedCommits(repo_path, rel_path_pp_files, repo_branch)
  # print pupp_commits_in_repo

  pupp_full_commit_data = getPuppCommitFullData(repo_path, repo_branch, pupp_commits_in_repo)
  print pupp_full_commit_data
 


if __name__=='__main__':
    orgName='wikimedia-downloads'
    #orgName='openstack-downloads'


    fileName="/Users/akond/PUPP_REPOS/"+orgName+'/'+'eligible_repos.csv'
    elgibleRepos = getEligibleProjects(fileName)

    for proj_ in elgibleRepos:
        print "="*75
        print "Processing ", proj_
        constructDataset(orgName, proj_, 'master')
        print "="*75  