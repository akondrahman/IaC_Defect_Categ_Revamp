'''
Akond Rahman 
June 01 2019 
Saturday 
'''
import pandas as pd 
import numpy as np 
import os 
import hglib 

def getBranchName(proj_):
    branch_name = ''
    proj_branch = {'biemond@biemond-oradb':'puppet4_3_data', 'derekmolloy@exploringBB':'version2', 'exploringBB':'version2', 
                   'jippi@puppet-php':'php7.0', 'maxchk@puppet-varnish':'develop', 'threetreeslight@my-boxen':'mine', 
                   'puppet':'production'
                  } 
    if proj_ in proj_branch:
        branch_name = proj_branch[proj_]
    else:
        branch_name = constants.MASTER_BRANCH
    return branch_name

def changeCategIfNeeded(categ_param):
    categ_mod = ''
    mod_dict  = {
                'BUILD_DEFECT':'SERVICE_DEFECT', 
                'DB_DEFECT':'SERVICE_DEFECT', 
                'INSTALL_DEFECT':'SERVICE_DEFECT', 
                'LOG_DEFECT':'SERVICE_DEFECT', 
                'NET_DEFECT':'SERVICE_DEFECT', 
                'RACE_DEFECT':'SERVICE_DEFECT'
                }
    if categ_param in mod_dict:
        categ_mod = mod_dict[categ_param]
    else:
        categ_mod = categ_param
    return categ_mod

def getFullCategFreq(file_name):
    categ_dict   = {}
    full_df      = pd.read_csv(file_name) 
    full_hash_ls =  np.unique( full_df['HASH'].tolist() )
    tot_hash_cnt = len(full_hash_ls)
    print 'DATASET:', file_name
    print 'TOTAL_COMMIT_COUNT:', tot_hash_cnt
    print '='*100
    for indi_hash in full_hash_ls:
        indi_hash_df    = full_df[full_df['HASH']==indi_hash] 
        indi_hash_categ = np.unique(indi_hash_df['CATEG'].tolist())

        for categ_ in indi_hash_categ:
            categ_ = changeCategIfNeeded(categ_)
            if categ_ not in categ_dict:
                categ_dict[categ_] = [indi_hash] 
            else:
                categ_dict[categ_] = [indi_hash] + categ_dict[categ_] 
    for categ, hash_list in categ_dict.iteritems():
        categ_count        = len(np.unique(hash_list))
        prop_defect_commit = (float(categ_count)/float(tot_hash_cnt))*100 
    
        print 'CATEG:{}, RAW_COUNT:{}, PROP_DEFECT_COMMIT:{}'.format(categ, categ_count, prop_defect_commit)
        print '*'*50 

def getOnlyDefectCategFreq(file_name):
    categ_dict   = {}
    full_df      = pd.read_csv(file_name) 
    full_hash_ls =  np.unique( full_df['HASH'].tolist() )
    tot_hash_cnt = len(full_hash_ls)

    only_defect_df      = full_df[full_df['CATEG']!='NO_DEFECT']
    only_defect_hash_ls = np.unique( only_defect_df['HASH'].tolist() )
    only_defect_count   = len(only_defect_hash_ls) 
    print 'DATASET:', file_name
    print 'ONLY_DEFECT_COMMIT_COUNT:', only_defect_count
    print '='*100
    for indi_hash in full_hash_ls:
        indi_hash_df    = only_defect_df[only_defect_df['HASH']==indi_hash] 
        indi_hash_categ = np.unique(indi_hash_df['CATEG'].tolist())

        for categ_ in indi_hash_categ:
            categ_ = changeCategIfNeeded(categ_)
            if categ_ not in categ_dict:
                categ_dict[categ_] = [indi_hash] 
            else:
                categ_dict[categ_] = [indi_hash] + categ_dict[categ_] 
    for categ, hash_list in categ_dict.iteritems():
        categ_count        = len(np.unique(hash_list))
        prop_defect_commit = (float(categ_count)/float(only_defect_count))*100 
    
        print 'CATEG:{}, RAW_COUNT:{}, ONLY_DEFECT_COUNT:{}, ONLY_DEFECT_PROP:{}'.format(categ, categ_count, only_defect_count, prop_defect_commit)
        print '*'*50 

def getAtLeastOne(file_param):
    print '='*100    
    full_df          = pd.read_csv(file_param) 
    full_hash_ls     =  np.unique( full_df['HASH'].tolist() )
    tot_hash_cnt     = len(full_hash_ls)
    print 'DATASET:', file_param
    print 'TOTAL_COMMIT_COUNT:', tot_hash_cnt
    only_defect_df   = full_df[full_df['CATEG']!='NO_DEFECT'] 
    only_defect_hash = np.unique( only_defect_df['HASH'].tolist()  )
    only_defect_cnt  = len(only_defect_hash)  
    atleast_one_hash = (float(only_defect_cnt) / float(tot_hash_cnt) ) *100
    print 'AT_LEAST_ONE_DEFECT_RELATED_COMMIT:{}, PERC:{}'.format(only_defect_cnt, atleast_one_hash) 
    print '='*100    


def getRepoDetails(_dir):
    all_files, iac_files = [] , []
    for root_, dirs, files_ in os.walk(_dir):
       for file_ in files_:
        full_p_file = os.path.join(root_, file_)
        all_files.append(full_p_file)

    for root_, dirs, files_ in os.walk(_dir):
       for file_ in files_:
           full_p_file = os.path.join(root_, file_)
           if (full_p_file.endswith('.pp')):
               iac_files.append(full_p_file)

    return all_files, iac_files

def getHgCommitCount(repo_name):
    repo_complete = hglib.open(repo_path)
    all_commits = repo_complete.log()

    return all_commits 

def getGitCommitCount(repo_name):
    proj_name  = repo_name.split('/')[-1]
    branchName = getBranchName(proj_name) 
    repo_  = Repo(repo_dir_absolute_path)
    all_commits = list(repo_.iter_commits(branchName))
    return all_commits     

def getSummary(out_fil):
    all_files, pp_files, all_commits = [], [], []
    df_ = pd.read_csv(out_fil) 
    pupp_hashes = np.unique( df_['HASH'].tolist() ) 
    repos = np.unique( df_['REPO'].tolist() ) 
    for repo_ in repos:
        repo_all_files, repo_pp_files = getRepoDetails(repo_) 
        all_files = all_files + repo_all_files 
        pp_files  = pp_files + repo_pp_files 
        if 'MOZI' in repo_: 
            all_commits = all_commits + getHgCommitCount(repo_)
        else:
            all_commits = all_commits + getGitCommitCount(repo_)
    pp_files_loc = [sum(1 for line in open(x_ , 'rU')) for x_ in pp_files if os.path.exists(x_) ]

    print '='*100
    print 'Total repo count:', len(repos)
    print 'Total commits:', len(all_commits) 
    print 'Total puppet-related commits:', len(pupp_hashes) 
    print 'Total files:', len(all_files) 
    print 'Total Puppet scripts:', len(pp_files) 
    print 'Total Puppet LOC:', sum(pp_files_loc) 
    print '='*100


if __name__=='__main__':
    acid_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/GHUB_CATEG_OUTPUT_FINAL.csv'
    # acid_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/MOZI_CATEG_OUTPUT_FINAL.csv'    
    # acid_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/OSTK_CATEG_OUTPUT_FINAL.csv'
    # acid_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/WIKI_CATEG_OUTPUT_FINAL.csv'


    # getAtLeastOne(acid_output_file)
    # getOnlyDefectCategFreq(acid_output_file)

    '''
    dataset summary: one time use 
    ''' 
    getSummary(acid_output_file) 