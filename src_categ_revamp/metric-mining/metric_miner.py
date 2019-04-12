'''
Get metrics for repos 
Akond Rahman 
April 12, 2019 
'''
import csv 
import numpy as np
import sys
from git import Repo
import  subprocess
import time 
import  datetime 
import os 
import cPickle as pickle 

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

    cmd_of_interrest1 = "cd " + repo_dir_absolute_path + " ; "
    cmd_of_interrest2 = "git show --name-status " + str(each_commit)  +  "  | awk '/.pp/ {print $2}'" 
    cmd_of_interrest = cmd_of_interrest1 + cmd_of_interrest2
    commit_of_interest  = subprocess.check_output(['bash' , '-c', cmd_of_interrest])

    for ppFile in ppListinRepo:
      if ppFile in commit_of_interest:

       file_with_path = os.path.join(repo_dir_absolute_path, ppFile)
       mapped_tuple = (file_with_path, each_commit)
       mappedPuppetList.append(mapped_tuple)

  return mappedPuppetList

def getDiffStr(repo_path_p, commit_hash_p, file_p):
   
   cdCommand   = "cd " + repo_path_p + " ; "
   theFile     = os.path.relpath(file_p, repo_path_p)
   
   diffCommand = " git diff  " + commit_hash_p + " " + theFile + " "
   command2Run = cdCommand + diffCommand
   diff_output = subprocess.check_output(['bash', '-c', command2Run])

   return diff_output

def getDiffLOC(diff_text):
    add_cnt, del_cnt = 0, 0 
    diff_text_list = diff_text.split('\n') 
    diff_text_list = [x_ for x_ in diff_text_list if (('---' not in x_) and ('+++' not in x_)) ]
    add_text_list  = [x_ for x_ in diff_text_list if x_.startswith('+')]
    del_text_list  = [x_ for x_ in diff_text_list if x_.startswith('-')]

    # print add_text_list, del_text_list 
    add_cnt, del_cnt = len(add_text_list), len(del_text_list)
    return add_cnt, del_cnt 

def getDevCountForFile(param_file_path, repo_path):
   author_count      = 1 

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   author_count        = len(np.unique(author_count_output))

   return author_count

def getDevsOfRepo(repo_path_param):
   author_dict       = {}

   cdCommand         = "cd " + repo_path_param + " ; "
   commitCountCmd    = " git log --pretty=format:'%H_%an' "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   for commit_auth in author_count_output:
       commit_ = commit_auth.split('_')[0]
       
       author_ = commit_auth.split('_')[1]
       author_ = author_.replace(' ', '')

       if commit_ not in author_dict:
           author_dict[commit_] = author_ 

   return author_dict  


def mineCommitsOfTheRepo(repo_path_param, repo_branch_param, pupp_commits_mapping):
    files_changed_dict, dirs_changed_dict = {}, {} 

    for tuple_ in pupp_commits_mapping:
        file_ = tuple_[0]
        commit_ = tuple_[1]
        msg_commit =  commit_.message 
        commit_hash = commit_.hexsha

        timestamp_commit = commit_.committed_datetime
        str_time_commit  = timestamp_commit.strftime('%Y-%m-%dT%H-%M-%S')

        diff_content_str = getDiffStr(repo_path_param, commit_hash, file_)
        loc_add, loc_del = getDiffLOC(diff_content_str) 
        loc_tot          = loc_add + loc_del 

        dir_             = os.path.dirname(file_) 
        devs_for_file    = getDevCountForFile(file_, repo_path_param) 

        metric_tuple = (file_, dir_, repo_path_param, loc_tot, devs_for_file)  
        print metric_tuple
        if commit_hash not in files_changed_dict:
           files_changed_dict[commit_hash] = [metric_tuple] 
        else: 
           files_changed_dict[commit_hash] = files_changed_dict[commit_hash] + [metric_tuple]  



def runMiner(orgParamName, repo_name_param, branchParam):
  
  repo_path   = '/Users/akond/PUPP_REPOS/' + orgParamName + "/" + repo_name_param
  repo_branch = branchParam

  all_devs_in_repo = getDevsOfRepo(repo_path)  
  print all_devs_in_repo 

  all_pp_files_in_repo = getPuppetFilesOfRepo(repo_path)
  
  rel_path_pp_files = getRelPathOfFiles(all_pp_files_in_repo, repo_path)

  pupp_commits_in_repo = getPuppRelatedCommits(repo_path, rel_path_pp_files, repo_branch)

  mineCommitsOfTheRepo(repo_path, repo_branch, pupp_commits_in_repo)
