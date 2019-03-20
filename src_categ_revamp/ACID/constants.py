'''
Akond Rahman 
Mar 19, 2019 
ACID: Store configuration strings and cosntants here 
'''

ROOT_PUPP_DIR  = '/Users/akond/PUPP_REPOS/' 
REPO_FILE_LIST = 'eligible_repos.csv'
MASTER_BRANCH  = 'master' 

ENCODING = 'utf8'
FILE_READ_MODE = 'rU' 
AST_PATH = 'EXTRA_AST' 

PP_EXTENSION = '.pp'
CHANGE_DIR_CMD = 'cd '
GIT_COMM_CMD_1 = "git show --name-status "
GIT_COMM_CMD_2 = "  | awk '/.pp/ {print $2}'" 
BASH_CMD = 'bash'
BASH_FLAG = '-c'

GIT_DIFF_CMD = " git diff  "
DATE_TIME_FORMAT = "%Y-%m-%dT%H-%M-%S"
FILE_WRITE_MODE = 'w'

NO_DEFECT_CATEG = 'NO_DEFECT'
CONFIG_DEFECT_CATEG = 'CONFIG_DEFECT'

prem_bug_kw_list      = ['error', 'bug', 'fix', 'issue', 'mistake', 'incorrect', 'fault', 'defect', 'flaw' ]
config_defect_kw_list = ['connection', 'string', 'parameter', 'hash', 'value', 'configure', 'field', 'option', 'version', 'URL', 'setting', 'ip', 'repo', 'link', 'time', 'server', 'command', 'setting', 'hiera', 'data', 'sql', 'permissions', 'mode', 'dir', 'protocol', 'missing', 'reference', 'path', 'location', 'driver', 'port', 'protocol', 'gateway', 'tcp', 'udp', 'fact']


DFLT_KW  = 'default'
CLOSE_KW = 'closes-bug'
