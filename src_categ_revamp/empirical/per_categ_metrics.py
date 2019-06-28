'''
Akond Rahman 
June 27, 2019 
Get Metrics Per Category 
'''
import pandas as pd 
import numpy as np 

metric_list = ['MOD_FILES', 'DIRS',	'TOT_SLOC',	'SPREAD', 'DEV_CNT_MOD_FILES', 'DEV_EXP', 'DEV_REXP']

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

def getMetricDist(categ_f, metric_f): 
    categ_df  = pd.read_csv(categ_f) 
    metric_df = pd.read_csv(metric_f) 
    result_df = pd.merge(categ_df, metric_df, on=['HASH'])
    result_df['CHANGED_CATEG'] = result_df['CATEG'].apply(changeCategIfNeeded) 
    categ_list = np.unique(result_df['CHANGED_CATEG'].tolist())
    for categ_ in categ_list:
        per_categ_df = result_df[result_df['CHANGED_CATEG']==categ_]
        print 'CATEGORY:',  categ_
        for metr_ in metric_list:
            metr_vals = per_categ_df[metr_].tolist() 
            if len(metr_vals) > 0 :
                print 'METRIC:{}, MIN:{}, MEDIAN:{}, AVG:{}, MAX:{}'.format(metr_,  min(metr_vals), np.median(metr_vals), np.mean(metr_vals), max(metr_vals) )
                print '-'*10
            else: 
                print 'METRIC:{}, MIN:{}, MEDIAN:{}, AVG:{}, MAX:{}'.format(metr_, 0, 0, 0, 0 )
                print '-'*10                
        print '*'*50

def getFileDist(categ_f, hash_mapping_f): 
    categ_df = pd.read_csv(categ_f) 
    map_df   = pd.read_csv(hash_mapping_f) 
    full_df  = pd.merge(categ_df, map_df, on=['HASH'])    
    # print full_df.tail() 
    all_files = list(np.unique(full_df['FILE'].tolist())) 
    print 'Total count of Puppet scripts:', len(all_files)
    print '='*50 
    atleat_one_files = []
    full_df['CHANGED_CATEG'] = full_df['CATEG'].apply(changeCategIfNeeded) 
    categ_list = np.unique(full_df['CHANGED_CATEG'].tolist())
    for categ_ in categ_list:
        per_categ_file_list = [] 
        for file_ in all_files:
            file_df = full_df[full_df['FILE']==file_]
            categ_file_df = file_df[file_df['CATEG']==categ_]
            files_categ   = list( np.unique(categ_file_df['FILE'].tolist() ) ) 
            per_categ_file_list = per_categ_file_list + files_categ
            if categ_!= 'NO_DEFECT': 
                atleat_one_files = atleat_one_files + files_categ 
        per_categ_file_prop = round(float(len(per_categ_file_list)) / float(len(all_files)), 5)* 100
        if categ_!= 'NO_DEFECT': 
            print 'CATEGORY:{}, SCRIPT_PROP(%):{}'.format(categ_, per_categ_file_prop) 
            print '*'*25
    atleast_one = round(float( atleat_one_files )   ) / float(len(all_files)), 5)* 100
    print 'Puppet scripts with at least one defect(%):', atleast_one 
    print '='*50     




if __name__=='__main__': 
    # categ_output_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/GHUB_CATEG_OUTPUT_FINAL.csv'
    # metric_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/GHUB_METRICS_OUTPUT_FINAL.csv' 
    # hash_mapping_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/GHUB_HASH_FILE_OUTPUT_FINAL.csv'

    # categ_output_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/MOZI_CATEG_OUTPUT_FINAL.csv'
    # metric_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/MOZI_METRICS_OUTPUT_FINAL.csv' 
    # hash_mapping_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/MOZI_HASH_FILE_OUTPUT_FINAL.csv'

    categ_output_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/OSTK_CATEG_OUTPUT_FINAL.csv'
    metric_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_METRICS_OUTPUT_FINAL.csv' 
    hash_mapping_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_HASH_FILE_OUTPUT_FINAL.csv' 

    # categ_output_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/output/WIKI_CATEG_OUTPUT_FINAL.csv'
    # metric_output_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_METRICS_OUTPUT_FINAL.csv' 
    # hash_mapping_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/WIKI_HASH_FILE_OUTPUT_FINAL.csv' 

    # getMetricDist(categ_output_file, metric_output_file)

    getFileDist(categ_output_file, hash_mapping_file) 