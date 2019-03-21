'''
Akond Rahman 
Mar 20, 2019 
Diff Parser that looks at diff content 
'''
#reff: https://github.com/cscorley/whatthepatch
import whatthepatch

import constants

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
    return_list = [x_.lower() for x_ in txt_lis if x_.startswith( constants.HASH_SYMBOL ) == False ]
    return_list = [x_.replace(constants.TAB, '') for x_ in return_list ]    
    return_list = [x_.replace(constants.NEWLINE, '') for x_ in return_list ]    
    return return_list

def getAddDelLines(diff_mess):
    added_text , deleted_text = [], []    
    for diff_ in whatthepatch.parse_patch(diff_mess):
        all_changes_line_by_line = diff_[1] ## diff_ is a tuple, changes is idnetified by the second index 
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
    if( any(x_ in added_text for x_ in constants.config_defect_kw_list) ) and ( any(x_ in deleted_text for x_ in constants.config_defect_kw_list) ):
            final_flag = True 
    elif ( any(constants.VAR_SIGN in x_ for x_ in added_text) ) and ( any(constants.VAR_SIGN in x_ for x_ in deleted_text) ):
            var_add_lis = [x_.replace(constants.WHITE_SPACE, '').split(constants.VAR_SIGN)[0] for x_ in added_text if constants.VAR_SIGN in x_ ]
            var_del_lis = [x_.replace(constants.WHITE_SPACE, '').split(constants.VAR_SIGN)[0] for x_ in deleted_text if constants.VAR_SIGN in x_ ] 
            var_common  = list(set(var_add_lis).intersection(var_del_lis)) 
            # print var_add_lis, var_del_lis
            # print var_common
            if len(var_common) > 0:
                final_flag = True
    return final_flag

def checkDiffForDepDefects(diff_text):
    added_text , deleted_text = [], []
    final_flag = False 
    added_text, deleted_text = getAddDelLines(diff_text)
    added_text   = filterTextList(added_text)
    deleted_text = filterTextList(deleted_text)
    if( any(x_ in added_text for x_ in constants.dep_defect_kw_list) ) or ( any(x_ in deleted_text for x_ in constants.dep_defect_kw_list) ):
            final_flag = True 
    return final_flag

    

        

            

