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

if __name__=='__main__':

    # orgName='wikimedia-downloads'
    # out_fil_nam = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_PUPP_COMM.PKL'
    # out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_CATEG_OUTPUT_FINAL.csv'
    # out_pkl_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_CATEG_OUTPUT_FINAL.PKL'

    orgName='openstack-downloads'
    out_fil_nam = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_PUPP_COMM.PKL'
    out_csv_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_CATEG_OUTPUT_FINAL.csv'
    out_pkl_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_CATEG_OUTPUT_FINAL.PKL'    

    fileName     = constants.ROOT_PUPP_DIR + orgName + '/' + constants.REPO_FILE_LIST 
    elgibleRepos = excavator.getEligibleProjects(fileName)
    dic   = {}
    categ = [] 
    for proj_ in elgibleRepos:
        per_proj_commit_dict, per_proj_full_defect_list = excavator.runMiner(orgName, proj_, constants.MASTER_BRANCH)
        categ = categ + per_proj_full_defect_list 
        print proj_ , len(per_proj_full_defect_list) 
        dic[proj_] = (per_proj_commit_dict, per_proj_full_defect_list) 
    
    all_proj_df = pd.DataFrame(categ) 
    all_proj_df.to_csv(out_csv_fil) 

    with open(out_pkl_fil, 'wb') as fp_:
        pickle.dump(dic, fp_)    

        
