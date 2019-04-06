'''
Akond Rahman 
Dec 02, 2018 
Mar 19, 2019: ACID: Extractor 
'''
import os 
import csv 
import numpy as np
import sys
from git import Repo
import  subprocess
import time 
import  datetime 
import cPickle as pickle 
from nltk.tokenize import sent_tokenize
import constants
import classifier

reload(sys)
sys.setdefaultencoding(constants.ENCODING) 

def getEligibleProjects(fileNameParam):
  repo_list = []
  with open(fileNameParam, constants.FILE_READ_MODE) as f:
    reader = csv.reader(f)
    for row in reader:
      repo_list.append(row[0])
  return repo_list

def getPuppetFilesOfRepo(repo_dir_absolute_path):
    pp_, non_pp = [], []
    for root_, dirs, files_ in os.walk(repo_dir_absolute_path):
       for file_ in files_:
           full_p_file = os.path.join(root_, file_)
           if((os.path.exists(full_p_file)) and (constants.AST_PATH not in full_p_file) ):
             if (full_p_file.endswith(constants.PP_EXTENSION)):
               pp_.append(full_p_file)
    return pp_

def getRelPathOfFiles(all_pp_param, repo_dir_absolute_path):
  common_path = repo_dir_absolute_path
  files_relative_paths = [os.path.relpath(path, common_path) for path in all_pp_param]
  return files_relative_paths 

def getPuppRelatedCommits(repo_dir_absolute_path, ppListinRepo, branchName=constants.MASTER_BRANCH):
  mappedPuppetList=[]
  track_exec_cnt = 0
  repo_  = Repo(repo_dir_absolute_path)
  all_commits = list(repo_.iter_commits(branchName))
  for each_commit in all_commits:
    track_exec_cnt = track_exec_cnt + 1

    cmd_of_interrest1 = constants.CHANGE_DIR_CMD + repo_dir_absolute_path + " ; "
    cmd_of_interrest2 = constants.GIT_COMM_CMD_1 + str(each_commit)  +  constants.GIT_COMM_CMD_2
    cmd_of_interrest = cmd_of_interrest1 + cmd_of_interrest2
    commit_of_interest  = subprocess.check_output([constants.BASH_CMD, constants.BASH_FLAG, cmd_of_interrest])

    for ppFile in ppListinRepo:
      if ppFile in commit_of_interest:

       file_with_path = os.path.join(repo_dir_absolute_path, ppFile)
       mapped_tuple = (file_with_path, each_commit)
       mappedPuppetList.append(mapped_tuple)

  return mappedPuppetList

def getDiffStr(repo_path_p, commit_hash_p, file_p):
   
   cdCommand   = constants.CHANGE_DIR_CMD + repo_path_p + " ; "
   theFile     = os.path.relpath(file_p, repo_path_p)
   
   diffCommand = constants.GIT_DIFF_CMD + commit_hash_p + constants.WHITE_SPACE + theFile + constants.WHITE_SPACE
   command2Run = cdCommand + diffCommand
   diff_output = subprocess.check_output([constants.BASH_CMD, constants.BASH_FLAG, command2Run])

   return diff_output

def makeDepParsingMessage(m_, i_): 
    upper, lower  = 0, 0
    lower = i_ - constants.STR_LIST_BOUNDS
    upper = i_ + constants.STR_LIST_BOUNDS 
    if upper > len(m_):
      upper = - 1 
    if lower < 0:
      lower = 0
    return constants.WHITE_SPACE.join(m_[i_ - constants.STR_LIST_BOUNDS : i_ + constants.STR_LIST_BOUNDS])

def processMessage(indi_comm_mess):
    splitted_messages = []
    if ('*' in indi_comm_mess):
       splitted_messages = indi_comm_mess.split('*')
    else:
       splitted_messages = sent_tokenize(indi_comm_mess)
    return splitted_messages 

def analyzeCommit(repo_path_param, repo_branch_param, pupp_commits_mapping):
  trac_exec_count = 0 
  pupp_bug_list = []
  all_commit_file_dict = {}
  for tuple_ in pupp_commits_mapping:
    file_ = tuple_[0]
    commit_ = tuple_[1]
    msg_commit =  commit_.message 

    msg_commit = msg_commit.replace('\n', constants.WHITE_SPACE)
    msg_commit = msg_commit.replace(',',  ';')    
    msg_commit = msg_commit.replace('\t', constants.WHITE_SPACE)
    msg_commit = msg_commit.replace('&',  ';')  
    msg_commit = msg_commit.replace('#',  constants.WHITE_SPACE)
    msg_commit = msg_commit.replace('=',  constants.WHITE_SPACE)      

    commit_hash = commit_.hexsha

    timestamp_commit = commit_.committed_datetime
    str_time_commit  = timestamp_commit.strftime(constants.DATE_TIME_FORMAT)

    diff_content_str = getDiffStr(repo_path_param, commit_hash, file_)

    tup_ = (repo_path_param, trac_exec_count, commit_hash, file_, str_time_commit, msg_commit, diff_content_str, repo_branch_param )
    # print tup_[0], tup_[1], tup_[2], tup_[3], tup_[4], tup_[5]

    bug_status, index_status = classifier.detectBuggyCommit(msg_commit)
    if bug_status:
      processed_message = processMessage(msg_commit)
      for tokenized_msg in processed_message:
          bug_categ = classifier.detectCateg(tokenized_msg, diff_content_str) 
          print tokenized_msg
          print commit_hash, bug_categ, repo_path_param, str_time_commit
          print '-'*100       
    else:
       bug_categ = constants.NO_DEFECT_CATEG

    if commit_hash not in all_commit_file_dict:
        all_commit_file_dict[commit_hash] = [file_]
    else:
        all_commit_file_dict[commit_hash]  = all_commit_file_dict[commit_hash] + [file_]    

    trac_exec_count += 1

  return all_commit_file_dict

def runMiner(orgParamName, repo_name_param, branchParam):
  
  repo_path   = constants.ROOT_PUPP_DIR + orgParamName + "/" + repo_name_param
  repo_branch = branchParam

  all_pp_files_in_repo = getPuppetFilesOfRepo(repo_path)
  
  rel_path_pp_files = getRelPathOfFiles(all_pp_files_in_repo, repo_path)

  pupp_commits_in_repo = getPuppRelatedCommits(repo_path, rel_path_pp_files, repo_branch)

  commit_file_dict = analyzeCommit(repo_path, repo_branch, pupp_commits_in_repo)
  # print 'Commit count:', len(commit_file_dict) 
  

def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, constants.FILE_WRITE_MODE)
  fileToWrite.write(strP )
  fileToWrite.close()
  return str(os.stat(fileP).st_size)

