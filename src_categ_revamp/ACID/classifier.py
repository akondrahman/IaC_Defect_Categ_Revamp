'''
Mar 20, 2019 
Akond Rahman 
Classify commit messages
'''
import constants 
import diff_parser

from nltk.tokenize import sent_tokenize
import re 
import spacy 
spacy_engine = spacy.load(constants.SPACY_ENG_DICT)
import future 
import numpy as np 
from nltk.stem.porter import *
stemmerObj = PorterStemmer()

def checkForNum(str_par):
    return any(char_.isdigit() for char_ in str_par)

def filterCommitMessage(msg_par):
    temp_msg_    = msg_par.lower()
    splitted_msg = temp_msg_.split(constants.WHITE_SPACE)
    splitted_msg = [stemmerObj.stem(x_) for x_ in splitted_msg] ##porter stemming 
    splitted_msg = [x_ for x_ in splitted_msg if len(x_) > 1 ]  ## remove special characterers 
    splitted_msg = [x_ for x_ in splitted_msg if x_.isalnum() ]  ## remove special characterers 
    filtered_msg = [x_ for x_ in splitted_msg if checkForNum(x_) == False ] ## remove alphanumeric characters     

    return filtered_msg 

def doDepAnalysis(msg_par):
    msg_to_analyze = []
    filtered_msg = filterCommitMessage(msg_par)
    unicode_msg_ = constants.WHITE_SPACE.join(filtered_msg)
    try:
        unicode_msg  = unicode(unicode_msg_, constants.UTF_ENCODING)
    except: 
        unicode_msg = unicode_msg_
    # print unicode_msg 
    spacy_doc = spacy_engine(unicode_msg)
    for token in spacy_doc:
        if (token.dep_ == constants.ROOT_TOKEN): 
            for x_ in token.children:
                msg_to_analyze.append(x_.text)
    return constants.WHITE_SPACE.join(msg_to_analyze) 

def detectBuggyCommit(msg_):
    flag2ret  = False 
    index2ret = 0
    msg_ = msg_.lower()
    if(any(x_ in msg_ for x_ in constants.prem_bug_kw_list)) and ( constants.DFLT_KW not in msg_) and ( constants.CLOSE_KW not in msg_) and (constants.MERGE_KW not in msg_) and (constants.REVERT_KW not in msg_):    
        str2see = [y_ for y_ in constants.prem_bug_kw_list][0]
        index2ret = msg_.find( str2see  ) 
        flag2ret = True 
    return flag2ret, index2ret

def detectCateg(msg_, diff_): 
    defect_categ = ''
    if (len(diff_) > 0):
        temp_msg_list = filterCommitMessage(msg_) # for extra false negative rules 
        # temp_msg_     = constants.WHITE_SPACE.join(temp_msg_list) # for extra false negative rules 

        msg_       = doDepAnalysis(msg_) ## depnding on results, this extra step of dependnecy parsing may change 
        # print 'Dependency analysis output:', msg_ 
        # diff_parse_dict = diff_parser.parseTheDiff(diff_) 
        # print 'Lines is the diff:', len(diff_parse_dict) 
        
        if(any(x_ in msg_ for x_ in constants.config_defect_kw_list)) and (diff_parser.checkDiffForConfigDefects(diff_)): 
            defect_categ = constants.CONFIG_DEFECT_CATEG
        elif(any(x_ in msg_ for x_ in constants.dep_defect_kw_list)) and (diff_parser.checkDiffForDepDefects(diff_)): 
            defect_categ = constants.DEP_DEFECT_CATEG        
        elif(any(x_ in msg_ for x_ in constants.doc_defect_kw_list )) and (diff_parser.checkDiffForDocDefects(diff_)) : 
            defect_categ = constants.DOC_DEFECT_CATEG
        elif(any(x_ in msg_ for x_ in constants.idem_defect_kw_list )) and (diff_parser.checkDiffForIdempotenceDefects(diff_)): 
            defect_categ = constants.IDEM_DEFECT_CATEG            
        elif(any(x_ in msg_ for x_ in constants.logic_defect_kw_list )) and (diff_parser.checkDiffForLogicDefects(diff_)) : 
            defect_categ = constants.LOGIC_DEFECT_CATEG                    
        elif(any(x_ in msg_ for x_ in constants.secu_defect_kw_list )) and (diff_parser.checkDiffForSecurityDefects(diff_)) : 
            defect_categ = constants.SECU_DEFECT_CATEG                                      
        elif(any(x_ in msg_ for x_ in constants.logging_defect_kw_list )) and (diff_parser.checkDiffForServiceDefects(diff_)) : 
            defect_categ = constants.LOGGING_DEFECT_CATEG   
        elif(any(x_ in msg_ for x_ in constants.network_defect_kw_list )) and (diff_parser.checkDiffForServiceDefects(diff_)): 
            defect_categ = constants.NETWORK_DEFECT_CATEG                             
        elif(any(x_ in msg_ for x_ in constants.service_defect_kw_list )) and (diff_parser.checkDiffForServiceDefects(diff_)): 
            defect_categ = constants.SERVICE_DEFECT_CATEG   
        elif(any(x_ in msg_ for x_ in constants.syntax_defect_kw_list )) and (diff_parser.checkDiffForSyntaxDefects(diff_)): 
            defect_categ = constants.SYNTAX_DEFECT_CATEG 
        #based on false negative analysis of Wikimedia 
        elif( any(y_ in temp_msg_list for y_ in constants.EXTRA_SYNTAX_KW )  ) and ( constants.EXTRA_FIX_KEYWORD in temp_msg_list):
            defect_categ = constants.SYNTAX_DEFECT_CATEG  
        elif( any(y_ in temp_msg_list for y_ in constants.EXTRA_CONFIG_KW )  ) and ( constants.EXTRA_FIX_KEYWORD in temp_msg_list):
            defect_categ = constants.CONFIG_DEFECT_CATEG                        
        elif( any(y_ in temp_msg_list for y_ in constants.EXTRA_SERVICE_KW )  ) and ( constants.EXTRA_FIX_KEYWORD in temp_msg_list):
            defect_categ = constants.SERVICE_DEFECT_CATEG  
        elif( any(y_ in temp_msg_list for y_ in constants.EXTRA_DEPENDENCY_KW )  ) and ( constants.EXTRA_FIX_KEYWORD in temp_msg_list):
            defect_categ = constants.DEP_DEFECT_CATEG                                     
        elif( any(y_ in temp_msg_list for y_ in constants.EXTRA_DOCU_KW )  ) and ( constants.EXTRA_FIX_KEYWORD in temp_msg_list) :
            defect_categ = constants.DOC_DEFECT_CATEG   
        elif( any(y_ in temp_msg_list for y_ in constants.idem_defect_kw_list ) ) and ( constants.EXTRA_FIX_KEYWORD in temp_msg_list) :
            defect_categ = constants.IDEM_DEFECT_CATEG            
        else: 
            defect_categ = constants.NO_DEFECT_CATEG
    else:
        defect_categ = constants.NO_DEFECT_CATEG        
    return defect_categ