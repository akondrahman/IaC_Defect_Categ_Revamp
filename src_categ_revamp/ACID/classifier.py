'''
Mar 20, 2019 
Akond Rahman 
Classify commit messages
'''
import constants 

def detectBuggyCommit(msg_):
    flag2ret  = False 
    msg_ = msg_.lower()
    if(any(x_ in msg_ for x_ in constants.prem_bug_kw_list)) and ( constants.DFLT_KW not in msg_) and ( constants.CLOSE_KW not in msg_):    
        flag2ret = True 
    return flag2ret

def detectCateg(msg_, diff_): 
    defect_categ = ''
    if (len(diff_) > 0):
        if(any(x_ in msg_ for x_ in constants.config_defect_kw_list)): 
            defect_categ = constants.CONFIG_DEFECT_CATEG
        elif(any(x_ in msg_ for x_ in constants.dep_defect_kw_list)): 
            defect_categ = constants.DEP_DEFECT_CATEG        
        elif(any(x_ in msg_ for x_ in constants.doc_defect_kw_list )): 
            defect_categ = constants.DOC_DEFECT_CATEG
        elif(any(x_ in msg_ for x_ in constants.idem_defect_kw_list )): 
            defect_categ = constants.IDEM_DEFECT_CATEG            
        elif(any(x_ in msg_ for x_ in constants.logic_defect_kw_list )): 
            defect_categ = constants.LOGIC_DEFECT_CATEG                    
        elif(any(x_ in msg_ for x_ in constants.secu_defect_kw_list )): 
            defect_categ = constants.SECU_DEFECT_CATEG  
        elif(any(x_ in msg_ for x_ in constants.build_defect_kw_list )): 
            defect_categ = constants.BLD_DEFECT_CATEG   
        elif(any(x_ in msg_ for x_ in constants.db_defect_kw_list )): 
            defect_categ = constants.DB_DEFECT_CATEG                                                           
        elif(any(x_ in msg_ for x_ in constants.insta_defect_kw_list )): 
            defect_categ = constants.INSTALL_DEFECT_CATEG                               
        elif(any(x_ in msg_ for x_ in constants.logging_defect_kw_list )): 
            defect_categ = constants.LOGGING_DEFECT_CATEG   
        elif(any(x_ in msg_ for x_ in constants.network_defect_kw_list )): 
            defect_categ = constants.NETWORK_DEFECT_CATEG                             
        elif(any(x_ in msg_ for x_ in constants.race_defect_kw_list )): 
            defect_categ = constants.RACE_DEFECT_CATEG 
        elif(any(x_ in msg_ for x_ in constants.service_defect_kw_list )): 
            defect_categ = constants.SERVICE_DEFECT_CATEG   
        elif(any(x_ in msg_ for x_ in constants.syntax_defect_kw_list )): 
            defect_categ = constants.SYNTAX_DEFECT_CATEG 
        else: 
            defect_categ = constants.NO_DEFECT_CATEG
    else:
        defect_categ = constants.NO_DEFECT_CATEG        
    return defect_categ