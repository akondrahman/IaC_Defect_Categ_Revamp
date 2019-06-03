'''
Akond Rahman 
Mar 19, 2019 : Tuesday 
ACID: Main 
'''
import excavator
import constants
import pandas as pd 
import cPickle as pickle


'''
This script goes to each repo and mines commits and commit messages and then get the defect category 
'''
def getBranchName(proj_):
    branch_name = ''
    proj_branch = {'biemond@biemond-oradb':'puppet4_3_data', 'derekmolloy@exploringBB':'version2', 'exploringBB':'version2', 
                   'jippi@puppet-php':'php7.0', 'maxchk@puppet-varnish':'develop', 'threetreeslight@my-boxen':'mine'
                  } 
    if proj_ in proj_branch:
        branch_name = proj_branch[proj_]
    else:
        branch_name = constants.MASTER_BRANCH
    return branch_name


if __name__=='__main__':

    # orgName     = 'oracle-dataset'
    # out_fil_nam = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/closed-coding-2019/ORACLE_DATASET_COMM.PKL'
    # out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/closed-coding-2019/ORACLE_CATEG_OUTPUT_SEMIFINAL.csv'
    # out_pkl_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/closed-coding-2019/ORACLE_CATEG_OUTPUT_SEMIFINAL.PKL'

    # orgName='ghub-downloads'
    # out_fil_nam = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/GHUB_PUPP_COMM.PKL'
    # out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/GHUB_CATEG_OUTPUT_FINAL.csv'
    # out_pkl_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/GHUB_CATEG_OUTPUT_FINAL.PKL'

    # orgName='wikimedia-downloads'
    # out_fil_nam = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/WIKI_PUPP_COMM.PKL'
    # out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/WIKI_CATEG_OUTPUT_FINAL.csv'
    # out_pkl_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/WIKI_CATEG_OUTPUT_FINAL.PKL'

    orgName='openstack-downloads'
    out_fil_nam = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/OSTK_PUPP_COMM.PKL'
    out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/OSTK_CATEG_OUTPUT_FINAL.csv'
    out_pkl_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/OSTK_CATEG_OUTPUT_FINAL.PKL'    

    fileName     = constants.ROOT_PUPP_DIR + orgName + '/' + constants.REPO_FILE_LIST 
    elgibleRepos = excavator.getEligibleProjects(fileName)
    dic   = {}
    categ = [] 
    for proj_ in elgibleRepos:
        branchName = getBranchName(proj_) 
        per_proj_commit_dict, per_proj_full_defect_list = excavator.runMiner(orgName, proj_, branchName)
        categ = categ + per_proj_full_defect_list 
        # print proj_ , len(per_proj_full_defect_list) 
        print 'Analyzing:', proj_
        dic[proj_] = (per_proj_commit_dict, per_proj_full_defect_list) 
        print '='*50 
    
    all_proj_df = pd.DataFrame(categ) 
    all_proj_df.to_csv(out_csv_fil) 

    with open(out_pkl_fil, 'wb') as fp_:
        pickle.dump(dic, fp_)    

        
