'''
Akond Rahman 
Mar 20, 2019 
Diff Parser that looks at diff content 
'''
#reff: https://github.com/cscorley/whatthepatch
import whatthepatch

import constants

from fuzzywuzzy import fuzz

# [(1, None, '# == Class cdh4::pig'), (None, 1, '# == Class cdh::pig'), (2, 2, '#'), (3, None, '# Installs and configures Apache Pig.'), (None, 3, '# Installs and configures Apache Pig and Pig DataFu.'), (4, 4, '#'), (5, None, 'class cdh4::pig {'), (6, None, "  package { 'pig':"), (7, None, "    ensure => 'installed',"), (8, None, '  }'), (None, 5, 'class cdh::pig('), (None, 6, "    $pig_properties_template = 'cdh/pig/pig.properties.erb',"), (None, 7, "    $log4j_template          = 'cdh/pig/log4j.properties.erb',"), (None, 8, ')'), (None, 9, '{'), (None, 10, '    # cdh::pig requires hadoop client and configs are installed.'), (None, 11, "    Class['cdh::hadoop'] -> Class['cdh::pig']"), (9, 12, ''), (10, None, "  file { '/etc/pig/conf/pig.properties':"), (11, None, "    content => template('cdh4/pig/pig.properties.erb'),"), (12, None, "    require => Package['pig'],"), (13, None, '  }'), (None, 13, "    package { 'pig':"), (None, 14, "        ensure => 'installed',"), (None, 15, '    }'), (None, 16, "    package { 'pig-udf-datafu':"), (None, 17, "        ensure => 'installed',"), (None, 18, '    }'), (None, 19, ''), (None, 20, '    $config_directory = "/etc/pig/conf.${cdh::hadoop::cluster_name}"'), (None, 21, '    # Create the $cluster_name based $config_directory.'), (None, 22, '    file { $config_directory:'), (None, 23, "        ensure  => 'directory',"), (None, 24, "        require => Package['pig'],"), (None, 25, '    }'), (None, 26, "    cdh::alternative { 'pig-conf':"), (None, 27, "        link    => '/etc/pig/conf',"), (None, 28, '        path    => $config_directory,'), (None, 29, '    }'), (None, 30, ''), (None, 31, '    file { "${config_directory}/pig.properties":'), (None, 32, '        content => template($pig_properties_template),'), (None, 33, "        require => Package['pig'],"), (None, 34, '    }'), (None, 35, '    file { "${config_directory}/log4j.properties":'), (None, 36, '        content => template($log4j_template),'), (None, 37, "        require => Package['pig'],"), (None, 38, '    }'), (14, 39, '}')]

def parseTheDiff(diff_text):
    parse_out_dict = {}
    for diff_ in whatthepatch.parse_patch(diff_text):
        all_changes_line_by_line = diff_[1] ## diff_ is a tuple, changes is idnetified by the second index 
        line_numbers_added, line_numbers_deleted = [], [] 
        add_dic, del_dic = {}, {}
        parse_out_dict   = {}
        for change_tuple in all_changes_line_by_line:
            if (change_tuple[0] != None ):
                line_numbers_added.append(change_tuple[0])
                add_dic[change_tuple[0]] = change_tuple[2]
            if (change_tuple[1] != None ):
                line_numbers_deleted.append(change_tuple[1])                
                del_dic[change_tuple[1]] = change_tuple[2]
        lines_changed = list(set(line_numbers_added).intersection(line_numbers_deleted)) 
        for line_number in lines_changed:
            if ((line_number in add_dic) and (line_number in del_dic)):
                parse_out_dict[line_number] = [ del_dic[line_number], add_dic[line_number]] ## <removed content, added cotnent>
        #print parse_out_dict
    return parse_out_dict

def filterTextList(txt_lis):
    return_list = []
    return_list = [x_.lower() for x_ in txt_lis if  constants.HASH_SYMBOL not in x_ ]
    return_list = [x_.replace(constants.TAB, '') for x_ in return_list ]    
    return_list = [x_.replace(constants.NEWLINE, '') for x_ in return_list ] 
    return_list = [x_ for x_ in return_list if len(x_) > 1 ]        
    return return_list

def getAddDelLines(diff_mess):
    added_text , deleted_text = [], []    
    for diff_ in whatthepatch.parse_patch(diff_mess):
        all_changes_line_by_line = diff_[1] ## diff_ is a tuple, changes is idnetified by the second index 
        if all_changes_line_by_line is not None:
            for change_tuple in all_changes_line_by_line:
                if (change_tuple[0] != None ):
                    added_text.append(change_tuple[2])
                if (change_tuple[1] != None ):
                    deleted_text.append(change_tuple[2])
    return added_text, deleted_text

def checkDiffForConfigDefects(diff_text):
    added_text , deleted_text = [], []
    final_flag = False 
    added_text, deleted_text = getAddDelLines(diff_text)
    added_text   = filterTextList(added_text)
    deleted_text = filterTextList(deleted_text)
    # if( any(x_ in added_text for x_ in constants.config_defect_kw_list) ) and ( any(x_ in deleted_text for x_ in constants.config_defect_kw_list) ):
    #         final_flag = True 
    # elif ( any(constants.VAR_SIGN in x_ for x_ in added_text) ) and ( any(constants.VAR_SIGN in x_ for x_ in deleted_text) ): ## for variables 
    #         var_add_lis = [x_.replace(constants.WHITE_SPACE, '').split(constants.VAR_SIGN)[0] for x_ in added_text if constants.VAR_SIGN in x_ ]
    #         var_del_lis = [x_.replace(constants.WHITE_SPACE, '').split(constants.VAR_SIGN)[0] for x_ in deleted_text if constants.VAR_SIGN in x_ ] 
    #         var_common  = list(set(var_add_lis).intersection(var_del_lis)) 
    #         if len(var_common) > 0:
    #             final_flag = True
    # elif ( any(constants.ATTR_SIGN in x_ for x_ in added_text) ) and ( any(constants.ATTR_SIGN in x_ for x_ in deleted_text) ): ## for attributes 
    #         attr_add_lis = [x_.replace(constants.WHITE_SPACE, '').split(constants.ATTR_SIGN)[0] for x_ in added_text if constants.ATTR_SIGN in x_ ]
    #         attr_del_lis = [x_.replace(constants.WHITE_SPACE, '').split(constants.ATTR_SIGN)[0] for x_ in deleted_text if constants.ATTR_SIGN in x_ ] 
    #         attr_common  = list(set(attr_add_lis).intersection(attr_del_lis)) 
    #         if len(attr_common) > 0:
    #             final_flag = True
    if ( any(constants.ATTR_SIGN in x_ for x_ in added_text) ) and ( any(constants.ATTR_SIGN in x_ for x_ in deleted_text) ): ## for RHS comparisons, detect msi matches, and they are indicative of code changes 
            attr_add_lis   = [x_.replace(constants.WHITE_SPACE, '').split(constants.ATTR_SIGN)[1] for x_ in added_text if constants.ATTR_SIGN in x_ ]
            attr_del_lis   = [x_.replace(constants.WHITE_SPACE, '').split(constants.ATTR_SIGN)[1] for x_ in deleted_text if constants.ATTR_SIGN in x_ ] 
            mismatches_del = [x_ for x_ in attr_del_lis if x_ not in attr_add_lis]
            mismatches_add = [x_ for x_ in attr_add_lis if x_ not in attr_del_lis]
            if (len(mismatches_add) > 0) or (len(mismatches_del) > 0):
                final_flag = True
    elif ( any(constants.VAR_SIGN in x_ for x_ in added_text) ) and ( any(constants.VAR_SIGN in x_ for x_ in deleted_text) ): ## for RHS comparisons, detect msi matches, and they are indicative of code changes 
            attr_add_lis   = [x_.replace(constants.WHITE_SPACE, '').split(constants.VAR_SIGN)[1] for x_ in added_text if constants.VAR_SIGN in x_ ]
            attr_del_lis   = [x_.replace(constants.WHITE_SPACE, '').split(constants.VAR_SIGN)[1] for x_ in deleted_text if constants.VAR_SIGN in x_ ] 
            mismatches_del = [x_ for x_ in attr_del_lis if x_ not in attr_add_lis]
            mismatches_add = [x_ for x_ in attr_add_lis if x_ not in attr_del_lis]
            if (len(mismatches_add) > 0) or (len(mismatches_del) > 0):
                final_flag = True
    return final_flag

def checkDiffForDepDefects(diff_text):
    added_text , deleted_text = [], []
    final_flag, final_flag_1, final_flag_2 = False , False, False 
    added_text, deleted_text = getAddDelLines(diff_text)
    added_text   = filterTextList(added_text)
    deleted_text = filterTextList(deleted_text)
    added_text   = [x_ for x_ in added_text if constants.VAR_SIGN not in x_ ]
    added_text   = [x_ for x_ in added_text if constants.ATTR_SIGN not in x_ ]

    deleted_text   = [x_ for x_ in deleted_text if constants.VAR_SIGN not in x_ ]
    deleted_text   = [x_ for x_ in deleted_text if constants.ATTR_SIGN not in x_ ]
    # print added_text, deleted_text
    added_text   = [z_ for z_ in added_text if any(x_ in z_ for x_ in constants.diff_depen_code_elems ) ]
    deleted_text = [z_ for z_ in deleted_text if any(x_ in z_ for x_ in constants.diff_depen_code_elems ) ] 

    if (len(added_text) > 0 ) and (len(deleted_text) > 0 ) :
       final_flag = True 

    return final_flag

def checkDiffForDocDefects(diff_text):
    lines_changed = []
    final_flag = False 
    for diff_ in whatthepatch.parse_patch(diff_text):
        all_changes_line_by_line = diff_[1] 
        line_numbers_added, line_numbers_deleted = [], [] 
        if all_changes_line_by_line is not None:
            for change_tuple in all_changes_line_by_line:
                content = change_tuple[2] 
                content = content.replace(constants.WHITE_SPACE, '')
                if (change_tuple[0] != None ) and ( content.startswith(constants.HASH_SYMBOL) ):
                    line_numbers_added.append( content )
                if (change_tuple[1] != None ) and ( content.startswith(constants.HASH_SYMBOL)  ):
                    line_numbers_deleted.append( content ) 
        lines_changed = list(set(line_numbers_added).intersection(line_numbers_deleted)) 
        # print lines_changed
    lines_changed = [x_ for x_ in lines_changed if len(x_) > 1 ]
    if len(lines_changed) > 0:
        final_flag = True
    return final_flag

    
def checkDiffForLogicDefects(diff_text):
    added_text , deleted_text = [], []
    final_flag, final_flag_1, final_flag_2 = False , False, False 
    added_text, deleted_text = getAddDelLines(diff_text)
    added_text   = filterTextList(added_text)
    deleted_text = filterTextList(deleted_text)
    added_text   = [x_ for x_ in added_text if constants.VAR_SIGN not in x_ ]
    added_text   = [x_ for x_ in added_text if constants.ATTR_SIGN not in x_ ]

    deleted_text   = [x_ for x_ in deleted_text if constants.VAR_SIGN not in x_ ]
    deleted_text   = [x_ for x_ in deleted_text if constants.ATTR_SIGN not in x_ ]
    # print added_text, deleted_text
    added_text   = [z_ for z_ in added_text if any(x_ in z_ for x_ in constants.diff_logic_code_elems ) ]
    deleted_text = [z_ for z_ in deleted_text if any(x_ in z_ for x_ in constants.diff_logic_code_elems ) ] 

    if (len(added_text) > 0 ) or (len(deleted_text) > 0 ) :
       final_flag = True 
    return final_flag
        
def checkDiffForSecurityDefects(diff_text):
    final_flag = False     
    added_text , deleted_text = [], []

    added_text, deleted_text = getAddDelLines(diff_text)
    added_text   = filterTextList(added_text)
    deleted_text = filterTextList(deleted_text)
    added_text   = [x_ for x_ in added_text if constants.VAR_SIGN  in x_ ]
    added_text   = [x_ for x_ in added_text if constants.ATTR_SIGN  in x_ ]

    deleted_text = [x_ for x_ in deleted_text if constants.VAR_SIGN  in x_ ]
    deleted_text = [x_ for x_ in deleted_text if constants.ATTR_SIGN  in x_ ]

    added_text   = [x_.split(constants.VAR_SIGN)[0].replace(constants.WHITE_SPACE, '') for x_ in added_text]
    added_text   = [x_.split(constants.ATTR_SIGN )[0].replace(constants.WHITE_SPACE, '') for x_ in added_text] 

    deleted_text   = [x_.split(constants.VAR_SIGN)[0].replace(constants.WHITE_SPACE, '') for x_ in deleted_text]
    deleted_text   = [x_.split(constants.ATTR_SIGN )[0].replace(constants.WHITE_SPACE, '') for x_ in deleted_text]    

    added_text   = [z_ for z_ in added_text if any(x_ in z_ for x_ in constants.diff_secu_code_elems ) ]
    deleted_text = [z_ for z_ in deleted_text if any(x_ in z_ for x_ in constants.diff_secu_code_elems ) ]    
    # print added_text, deleted_text
    if (len(added_text) > 0) or (len(deleted_text) > 0): 
        final_flag = True
    return final_flag
            
def checkDiffForServiceDefects(diff_text):
    final_flag = False 
    added_text , deleted_text = [], []

    added_text, deleted_text = getAddDelLines(diff_text)
    added_text   = filterTextList(added_text)
    deleted_text = filterTextList(deleted_text)
    added_text   = [x_ for x_ in added_text if constants.VAR_SIGN  not in x_ ]
    added_text   = [x_.lower() for x_ in added_text if constants.ATTR_SIGN not in x_ ]

    deleted_text = [x_ for x_ in deleted_text if constants.VAR_SIGN not in x_ ]
    deleted_text = [x_.lower() for x_ in deleted_text if constants.ATTR_SIGN not in x_ ]

    added_text   = [z_ for z_ in added_text if any(x_ in z_ for x_ in constants.diff_service_code_elems) ]
    deleted_text = [z_ for z_ in deleted_text if any(x_ in z_ for x_ in constants.diff_service_code_elems) ] 

    if (len(added_text) > 0 ) and (len(deleted_text) > 0 ) :
       final_flag = True 
    return final_flag

def matchStringsFuzzily(add_str_lis, del_str_lis):
    # takes two sring as input, returns levesjhteins's ratio, reff: https://www.datacamp.com/community/tutorials/fuzzy-string-python
    add_str = constants.WHITE_SPACE.join(add_str_lis)
    del_str = constants.WHITE_SPACE.join(del_str_lis) 
    lower_add_str = add_str.lower() 
    lower_del_str = del_str.lower()
    lev_str_ratio = fuzz.token_sort_ratio( lower_add_str, lower_del_str  ) ## this is levenshteien ratio, in a sorted manner 
    return lev_str_ratio


def checkDiffForSyntaxDefects(diff_text):
    final_flag = False 
    added_text , deleted_text = [], []
    attr_added_text , attr_deleted_text = [], []
    var_added_text , var_deleted_text = [], []

    added_text, deleted_text = getAddDelLines(diff_text)
    added_text   = filterTextList(added_text)
    deleted_text = filterTextList(deleted_text)

    '''
    look for variable name change 
    '''
    attr_added_text   = [x_.lower() for x_ in added_text if constants.ATTR_SIGN in x_ ]
    var_added_text    = [x_.lower().replace(constants.WHITE_SPACE, '') for x_ in added_text if constants.VAR_SIGN in x_ ]

    attr_deleted_text = [x_.lower() for x_ in deleted_text if constants.ATTR_SIGN in x_ ]
    var_deleted_text  = [x_.lower().replace(constants.WHITE_SPACE, '') for x_ in deleted_text if constants.VAR_SIGN in x_ ]
    '''
    Now compare 
    '''

    # if (len(added_text)) and (len(deleted_text)): ## wrong logic 
    if ((len(attr_added_text)) == (len(attr_deleted_text))) or (len(var_added_text) == len(var_deleted_text) ) : ## right logic , same number of additions and deletiosn for variables 
        final_flag = True 
    elif ( (matchStringsFuzzily(attr_added_text, attr_deleted_text) > constants.lev_cutoff ) or (matchStringsFuzzily(var_added_text, var_deleted_text) > constants.lev_cutoff ) ):
        final_flag - True 


    return final_flag



def checkDiffForIdempotenceDefects(diff_text):
    final_flag = False 
    added_text , deleted_text = [], []

    added_text, deleted_text = getAddDelLines(diff_text)
    added_text   = filterTextList(added_text)
    deleted_text = filterTextList(deleted_text)

    added_text = [x_ for x_ in added_text if constants.diff_idem_code_elem in x_ ] 
    if (len(added_text) == 1) or (len(deleted_text) > constants.diff_idem_removal_cnt):
       final_flag = True 

    return final_flag 

def checkDiffForIdemWithAttr(diff_text):
    final_flag = False 
    flag_list  = []
    added_text , deleted_text = [], []

    added_text, deleted_text = getAddDelLines(diff_text)
    added_text   = filterTextList(added_text)
    deleted_text = filterTextList(deleted_text)

    if(len(deleted_text) < len(added_text)):
        for text_ in added_text:
            for elem in constants.diff_extra_idem_elems:
                if elem in text_:
                    flag_list.append(True) 
    if (len(flag_list) > 0):    
        final_flag = True 
    return final_flag 
    