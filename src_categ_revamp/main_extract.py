'''
Akond Rahman 
Dec 02, 2018 
Revamping Defect Categ project : Extraction 
'''
import os 
import csv 
import numpy as np
import sys

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
           if((os.path.exists(full_p_file)) ):
             if (full_p_file.endswith('.pp')):
               pp_.append(full_p_file)
    return pp_


def constructDataset(orgParamName, repo_name_param, branchParam):

  repo_path   = "/Users/akond/PUPP_REPOS/" + orgParamName + "/" + repo_name_param
  repo_branch = branchParam

  all_pp_files_in_repo = getPuppetFilesOfRepo(repo_path)
  print all_pp_files_in_repo
  
  # rel_path_pp_files = bug_git_util.getRelPathOfFiles(all_pp_files_in_repo, repo_path)
  # pupp_commits_in_repo = bug_git_util.getPuppRelatedCommits(repo_path, rel_path_pp_files, repo_branch)
  # all_pupp_msgs = bug_git_util.getPuppMessages(yes_bug_mapping, no_bug_mapping)
  # unique_pupp_msg = np.unique(all_pupp_msgs)
  # all_pupp_msgs, pupp_to_msgs_dict = bug_git_util.getPuppMessages(yes_bug_mapping, no_bug_mapping)
 


if __name__=='__main__':
    orgName='wikimedia-downloads'
    #orgName='openstack-downloads'
    fileName="/Users/akond/PUPP_REPOS/"+orgName+'/'+'eligible_repos.csv'
    elgibleRepos = getEligibleProjects(fileName)
    '''
    Call the function
    '''
    for proj_ in elgibleRepos:
        print "="*75
        print "Processing ", proj_
        constructDataset(orgName, proj_, 'master')
        print "="*75  