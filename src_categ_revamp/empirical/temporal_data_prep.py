'''
Run script to get month wise defects 
Akond Rahman 
June 15, 2019 
'''

import numpy as np 
import pandas as pd 

categ_list = ['SERVICE_DEFECT', 'SECU_DEFECT', 'DEP_DEFECT', 'DOC_DEFECT', 'CONFIG_DEFECT', 'SYNTAX_DEFECT', 'CONDI_DEFECT', 'IDEM_DEFECT']

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

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

def makeMonth(time_single_val):
    date_ = time_single_val.split('T')[0] 
    date_list = date_.split('-')
    month = date_list[0] + '-' + date_list[1] 
    return month 

def makeTimeWiseDataset(file_name):
    str_builder  = ''
    acid_df  = pd.read_csv(file_name)
    acid_df['MONTH'] = acid_df['TIME'].apply(makeMonth)
    acid_df['CHANGED_CATEG'] = acid_df['CATEG'].apply(changeCategIfNeeded)
    print acid_df.head() 
    acid_all_months =  np.unique( acid_df['MONTH'].tolist() ) 
    for per_month in acid_all_months: 
        per_mon_df = acid_df[acid_df['MONTH']==per_month]
        per_mon_commits = np.unique( per_mon_df['HASH'].tolist() )
        commit_cnt  = len(per_mon_commits)
        for categ_ in categ_list: 
            per_mon_categ_df = per_mon_df[per_mon_df['CHANGED_CATEG']==categ_]
            per_categ_hashes = np.unique( per_mon_categ_df['HASH'].tolist() )
            categ_cnt = len(per_categ_hashes) 
            categ_perc = round(float(categ_cnt)/float(commit_cnt) , 5) * 100 
            str_builder = str_builder + per_month + ',' + categ_ + ',' + str(categ_perc) + '\n' 
    dump_file_name = file_name.split('/')[-1].split('_')[0] + '.csv' 
    str_builder = 'MONTH,CATEG,CATEG_PERC' + '\n' + str_builder
    dumpContentIntoFile(str_builder, dump_file_name)
    
 


if __name__=='__main__':
    # acid_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/GHUB_CATEG_OUTPUT_FINAL.csv'
    # acid_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/MOZI_CATEG_OUTPUT_FINAL.csv'    
    # acid_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/OSTK_CATEG_OUTPUT_FINAL.csv'
    acid_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/WIKI_CATEG_OUTPUT_FINAL.csv'

    makeTimeWiseDataset(acid_output_file)