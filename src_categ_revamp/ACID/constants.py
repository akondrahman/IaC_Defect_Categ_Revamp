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
