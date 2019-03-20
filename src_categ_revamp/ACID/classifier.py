'''
Mar 20, 2019 
Akond Rahman 
Classify commit messages
'''
import constants 

def detectBuggyCommit(msg_):
    flag2ret  = False 

    for msg_ in msg_lis:
        msg_ = msg_.lower()
        if(any(x_ in msg_ for x_ in constants.prem_bug_kw_list)) and ( constants.DFLT_KW not in msg_) and ( constants.CLOSE_KW not in msg_):    
          flag2ret = True 
    return flag2ret

def detectCateg(msg_, diff_): 
    defect_categ = ''
    if (len(diff_) > 0):
        if(any(x_ in msg_ for x_ in constants.config_defect_kw_list)): 
            defect_categ = constants.CONFIG_DEFECT_CATEG
        
