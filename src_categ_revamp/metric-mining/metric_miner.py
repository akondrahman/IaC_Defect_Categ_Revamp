'''
Get metrics for repos 
Akond Rahman 
April 12, 2019 
'''

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

def runMiner(orgParamName, repo_name_param, branchParam):
  
  repo_path   = constants.ROOT_PUPP_DIR + orgParamName + "/" + repo_name_param
  repo_branch = branchParam

  all_pp_files_in_repo = getPuppetFilesOfRepo(repo_path)
  
  rel_path_pp_files = getRelPathOfFiles(all_pp_files_in_repo, repo_path)

  pupp_commits_in_repo = getPuppRelatedCommits(repo_path, rel_path_pp_files, repo_branch)

  print len(pupp_commits_in_repo) 