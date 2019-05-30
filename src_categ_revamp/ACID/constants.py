'''
Akond Rahman 
Mar 19, 2019 
ACID: Store configuration strings and cosntants here 
'''

ROOT_PUPP_DIR  = '/Users/akond/ICSE2020_PUPP_REPOS/' 
REPO_FILE_LIST = 'eligible_repos.csv'
MASTER_BRANCH  = 'master' 
FILE_READ_MODE = 'rU' 
AST_PATH = 'EXTRA_AST' 
PP_EXTENSION = '.pp'
DATE_TIME_FORMAT = "%Y-%m-%dT%H-%M-%S"
WHITE_SPACE  = ' '
TAB = '\t'
NEWLINE = '\n'
HASH_SYMBOL = '#'

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

STR_LIST_BOUNDS  = 3 # tri-grams 
NO_DEFECT_CATEG        = 'NO_DEFECT'
CONFIG_DEFECT_CATEG    = 'CONFIG_DEFECT'
DEP_DEFECT_CATEG       = 'DEP_DEFECT'
DOC_DEFECT_CATEG       = 'DOC_DEFECT'
IDEM_DEFECT_CATEG      = 'IDEM_DEFECT'
CONDI_DEFECT_CATEG     = 'CONDI_DEFECT'
SECU_DEFECT_CATEG      = 'SECU_DEFECT'
BLD_DEFECT_CATEG       = 'BUILD_DEFECT'
DB_DEFECT_CATEG        = 'DB_DEFECT' 
INSTALL_DEFECT_CATEG   = 'INSTALL_DEFECT' 
LOGGING_DEFECT_CATEG   = 'LOG_DEFECT'
NETWORK_DEFECT_CATEG   = 'NET_DEFECT'
RACE_DEFECT_CATEG      = 'RACE_DEFECT'
SERVICE_DEFECT_CATEG   = 'SERVICE_DEFECT'
SYNTAX_DEFECT_CATEG    = 'SYNTAX_DEFECT'

prem_bug_kw_list      = ['error', 'bug', 'fix', 'issue', 'mistake', 'incorrect', 'fault', 'defect', 'flaw', 'solve' ]
# config_defect_kw_list = ['connection', 'string', 'paramet', 'hash', 'value', 'config', 'field', 'option', 'version', 'url', 'setting', 'ip', 'repo', 'link', 'time', 'server', 'command', 'setting', 'hiera', 'data', 'sql', 'permiss', 'mode', 'dir', 'protocol', 'missing', 'reference', 'path', 'location', 'driver', 'port', 'protocol', 'gateway', 'tcp', 'udp', 'fact', 'id']
config_defect_kw_list = ['connection', 'string', 'hash', 'value', 'config', 'field', 'option', 'version', 'setting', 'hiera', 'data']
# dep_defect_kw_list    = ['requir', 'depend', 'relation', 'order', 'sync', 'compatibility', 'ordering', 'missing', 'ensure', 'packag', 'conflict', 'name', 'inherit', 'module', 'merge', 'namespace', 'test', 'includ']
dep_defect_kw_list    = ['requir', 'depend', 'relation', 'order', 'sync', 'compatibil', 'ordering', 'missing', 'ensure', 'packag', 'inherit', 'module', 'includ']
doc_defect_kw_list    = ['doc', 'comment', 'spec', 'license', 'copyright', 'notice', 'header'] 
idem_defect_kw_list   = ['idempoten', 'idem']
logic_defect_kw_list  = ['logic', 'condition', 'boolean']
# secu_defect_kw_list   = ['vulnerability', 'ssl', 'firewall', 'secret', 'authenticate', 'tls', 'ca_file', 'password', 'security', 'cve']
secu_defect_kw_list   = ['vulnerability', 'ssl', 'firewall', 'secret', 'authenticate', 'password', 'security', 'cve']

# build_defect_kw_list  = ['build']
# db_defect_kw_list     = ['db', 'database', 'databas']
# insta_defect_kw_list  = ['install']
# race_defect_kw_list   = ['race']
logging_defect_kw_list= ['log']
# network_defect_kw_list= ['provis', 'provision', 'network', 'l23', 'balancer', 'domain', 'route', 'proxy', 'dhcp']
network_defect_kw_list= ['provis', 'network', 'proxy', 'dhcp']
# service_defect_kw_list= ['install', 'race', 'build', 'service', 'caching', 'backend', 'job', 'start', 'gate', 'stage', 'env', 'requirement', 'restore', 'server']
service_defect_kw_list= ['race', 'build', 'service', 'requirement', 'restore', 'server']

# syntax_defect_kw_list = ['compil', 'class', 'lint', 'warn', 'clean', 'typo', 'comma', 'style', 'wrong', 'quote', 'cosmetic', 'compil', 'variable', 'spelling', 'declar', 'missing', 'indent', 'definition', 'regex', 'type', 'format', 'duplicat', 'deprecate', 'parameter', 'outdate', 'variabl']
syntax_defect_kw_list = ['compil', 'lint', 'warn', 'clean', 'typo', 'style', 'quote', 'cosmetic', 'compil', 'variable', 'spelling', 'declar', 'indent', 'regex', 'type', 'format', 'duplicat', 'variabl']

EXTRA_SYNTAX_KW       = ['definition', 'role', 'whitespace', 'parameter', 'lint', 'style', 'typo', 'variable', 'indent', 'test', 'pattern', 'duplicate'] 
EXTRA_CONFIG_KW       = ['url', 'version', 'config', 'sql', 'tcp', 'hiera', 'repo', 'vlan', 'connection']  
EXTRA_DEPENDENCY_KW   = ['dep', 'ensur', 'requir', 'modul', 'packag']  
EXTRA_SERVICE_KW      = ['test', 'setup', 'site', 'restart', 'deploy', 'start', 'driver']  
EXTRA_DOCU_KW         = ['readme', 'doc', 'comment', 'license'] 
EXTRA_FIX_KEYWORD     = 'fix'   
EXTRA_SOLVE_KEYWORD   = 'solve'


DFLT_KW         = 'default'
CLOSE_KW        = 'closes-bug'
MERGE_KW        = 'merge' 
REVERT_KW       = 'revert'
REVERT_REGEX    = r'^revert.*\".*\"'
IDEM_XTRA_KW    = 'idem'
LOGIC_XTRA_KW   = 'condit'
SYNTAX_XTRA_KW1 = 'lint'
SYNTAX_XTRA_KW2 = 'typo'
SYNTAX_XTRA_KW3 = 'space'
DOC_XTRA_KW     = 'notice' 
DEPEND_XTRA_KW  = 'override' 
NETWORK_XTRA_KW = 'provis'

diff_config_code_elems = ['hiera' , 'hash', 'parameter', 'user']
VAR_SIGN = '='
ATTR_SIGN = '=>'
diff_depen_code_elems = ['~>' , '::', 'include', 'packag']
diff_logic_code_elems = ['if' , 'unless', 'els', 'case']
diff_secu_code_elems  = ['tls', 'cert', 'cred', 'ssl', 'password', 'pass', 'pwd'] 
diff_service_code_elems = ['service', 'exec'] 
diff_syntax_code_elems = ['class']
diff_idem_code_elem    = 'class' 
diff_idem_removal_cnt  = 10 

diff_extra_idem_elems  = ['ensure', 'unless', 'creates', 'replace'] 

'''
Oracle dataset work 
'''
ORACLE_HASH_CHECKLIST = ['52f0888af273e0ae9867ee6b5b645e0565732428', 
                         '975d8ef0fb352f689f78ecb9c33e0aef4062d45e', 
                         '114536ef2e7c569300019844e0ca57d278e27791',
                         'a7dedf197a24bf8a3fad00d1d1f58eede2f43057' 
                        ]