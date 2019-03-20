'''
Akond Rahman 
Mar 19, 2019 
ACID: Store configuration strings and cosntants here 
'''

ROOT_PUPP_DIR  = '/Users/akond/PUPP_REPOS/' 
REPO_FILE_LIST = 'eligible_repos.csv'
MASTER_BRANCH  = 'master' 
FILE_READ_MODE = 'rU' 
AST_PATH = 'EXTRA_AST' 
PP_EXTENSION = '.pp'
DATE_TIME_FORMAT = "%Y-%m-%dT%H-%M-%S"
WHITE_SPACE  = ' '

CHANGE_DIR_CMD = 'cd '
GIT_COMM_CMD_1 = "git show --name-status "
GIT_COMM_CMD_2 = "  | awk '/.pp/ {print $2}'" 
BASH_CMD = 'bash'
BASH_FLAG = '-c'
GIT_DIFF_CMD = " git diff  "

ENCODING = 'utf8'
UTF_ENCODING = 'utf-8'
FILE_WRITE_MODE = 'w'
SPACY_ENG_DICT  = 'en_core_web_sm'
ROOT_TOKEN = 'ROOT'

NO_DEFECT_CATEG = 'NO_DEFECT'
CONFIG_DEFECT_CATEG = 'CONFIG_DEFECT'
DEP_DEFECT_CATEG  = 'DEP_DEFECT'
DOC_DEFECT_CATEG  = 'DOC_DEFECT'
IDEM_DEFECT_CATEG = 'IDEM_DEFECT'
LOGIC_DEFECT_CATEG = 'LOGIC_DEFECT'
SECU_DEFECT_CATEG = 'SECU_DEFECT'
BLD_DEFECT_CATEG  = 'BUILD_DEFECT'
DB_DEFECT_CATEG   = 'DB_DEFECT' 
INSTALL_DEFECT_CATEG   = 'INSTALL_DEFECT' 
LOGGING_DEFECT_CATEG   = 'LOG_DEFECT'
NETWORK_DEFECT_CATEG   = 'NET_DEFECT'
RACE_DEFECT_CATEG      = 'RACE_DEFECT'
SERVICE_DEFECT_CATEG   = 'SERVICE_DEFECT'
SYNTAX_DEFECT_CATEG    = 'SYNTAX_DEFECT'

prem_bug_kw_list      = ['error', 'bug', 'fix', 'issue', 'mistake', 'incorrect', 'fault', 'defect', 'flaw' ]
config_defect_kw_list = ['connection', 'string', 'parameter', 'hash', 'value', 'config', 'field', 'option', 'version', 'URL', 'setting', 'ip', 'repo', 'link', 'time', 'server', 'command', 'setting', 'hiera', 'data', 'sql', 'permissions', 'mode', 'dir', 'protocol', 'missing', 'reference', 'path', 'location', 'driver', 'port', 'protocol', 'gateway', 'tcp', 'udp', 'fact']
dep_defect_kw_list    = ['dependency', 'relation', 'sync', 'compatibility', 'ordering', 'missing', 'ensure', 'package', 'conflict', 'name', 'inherit', 'module', 'merge', 'namespace', 'test']
doc_defect_kw_list    = ['doc', 'comment', 'spec', 'license', 'copyright', 'notice'] 
idem_defect_kw_list   = ['idempoten']
logic_defect_kw_list  = ['logic', 'way', 'conditional', 'boolean']
secu_defect_kw_list   = ['vulnerability', 'ssl', 'firewall', 'secret', 'authenticate', 'tls', 'ca_file', 'password', 'security']

build_defect_kw_list  = ['build']
db_defect_kw_list     = ['db', 'database']
insta_defect_kw_list  = ['install']
logging_defect_kw_list= ['log']
network_defect_kw_list= ['provision', 'network', 'l23', 'balancer', 'domain', 'route', 'proxy', 'dhcp']
race_defect_kw_list   = ['race']
service_defect_kw_list= ['service', 'caching', 'backend', 'job', 'start', 'gate', 'stage', 'env', 'requirement', 'restore', 'server']

syntax_defect_kw_list = ['class', 'lint', 'warning', 'clean', 'typo', 'comma', 'style', 'wrong', 'quote', 'cosmetic', 'compilation', 'variable', 'spelling', 'declaration', 'missing', 'indent', 'definition', 'regex', 'type', 'format', 'duplicate', 'deprecate', 'parameter', 'outdate']

DFLT_KW  = 'default'
CLOSE_KW = 'closes-bug'
