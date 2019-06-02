'''
Akond Rahman 
June 01 2019 
Saturday 
'''
import pandas as pd 
import numpy as np 

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

def getCategFreq(file_name):
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


if __name__=='__main__':
    acid_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/OSTK_CATEG_OUTPUT_FINAL.csv'
    getCategFreq(acid_output_file)