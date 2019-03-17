'''
Named entity recognition 
'''
# import nltk
# from nltk.tag import StanfordNERTagger
# #reff-1: https://medium.com/explore-artificial-intelligence/introduction-to-named-entity-recognition-eda8c97c2db1
# #reff-2: https://nlp.stanford.edu/software/CRF-NER.html#Download


# print 'NTLK Version:', nltk.__version__
# stanford_ner_tagger = StanfordNERTagger(
#     '/Users/akond/stanford_ner/' + 'english.muc.7class.distsim.crf.ser.gz',
#     '/Users/akond/stanford_ner/' + 'stanford-ner.jar'
# )


# article = '''Asian shares skidded on Tuesday after a rout in tech stocks put Wall Street to the sword, while 
# a sharp drop  in oil prices and political risks in Europe pushed the dollar to 16-month highs as investors dumped riskier assets. 
# MSCI's broadest index of Asia-Pacific shares outside Japan dropped 1.7 percent to a 1-1/2 week trough, with Australian shares sinking 1.6 
# percent. Sterling fell to $1.286 after three straight sessions of losses took it to the lowest since Nov.1 as there were still considerable 
# unresolved issues with the European Union over Brexit, British Prime Minsiter Theresa May said on Monday.'''

# results = stanford_ner_tagger.tag(article.split())
# for result in results:
#     tag_value = result[0]
#     tag_type = result[1]
#     if tag_type != 'O':
#         print 'Type: {}, Value: {}'.format ( tag_type, tag_value )
#         print '-'*50



# '''
# Dependnecy parsing 
# '''
# import spacy
# import future 
# #reff: https://spacy.io/usage/linguistic-features

# nlp = spacy.load('en_core_web_sm')
# doc = nlp(u"Autonomous cars shift insurance liability toward manufacturers")
# doc = nlp(u"Change section name for AMQP rabbit parameters  Parameter 'amqp_durable_queues' under section 'DEFAULT' now is deprecated since Liberty and should be placed under certain rpc backend section [1;2]  [1] https://github.com/openstack/oslo.messaging/blob/liberty/oslo_messaging/_drivers/amqp.py L36 [2] http://docs.openstack.org/liberty/config-reference/content/configuring-rpc.html  Change-Id: Ib7bbea586b21c42eb9fd13c4a376d23fce165272 ")
# for token in doc:
#     print(token.text, token.dep_, token.head.text, token.head.pos_,
#           [child for child in token.children])

'''
Dependency parsing setup for ACID 
Akond Rahman 
Mar 17, 2019 
'''
import pandas as pd 
from nltk.tokenize import sent_tokenize
import re 
import spacy 
spacy_engine = spacy.load('en_core_web_sm')
import future 
import numpy as np 

def removeFat(mess):
    #the_regex = re.compile(r'^[a-f0-9]{40}(:.+)?$', re.IGNORECASE)
    out_mes   = re.sub(r'^[a-f0-9]{40}(:.+)?$', '', mess)
    print out_mes


def detectBuggyCommitMessages(msg_lis):
    # print msg_lis
    for msg_ in msg_lis:
        msg_ = msg_.lower()
        if(('error' in msg_) or ('bug' in msg_ ) or ('fix' in msg_) or ('issue' in msg_) or ('mistake' in msg_) or ('incorrect' in msg_) or ('fault' in msg_) or ('defect' in msg_) or ('flaw' in msg_)) and ('default' not in msg_):
            unicode_msg  = unicode(msg_, 'utf-8')
            spacy_doc = spacy_engine(unicode_msg)
            for token in spacy_doc:
                if (token.dep_ == 'ROOT'):
                    print msg_
                    print(token.text, token.dep_, token.head.text, token.head.pos_, [x_ for x_ in token.children])  
                    print '-'*100

def processMessage(indi_comm_mess):
    if ('*' in indi_comm_mess):
       splitted_messages = indi_comm_mess.split('*')
    else:
       splitted_messages = sent_tokenize(indi_comm_mess)
    # print splitted_messages 
    detectBuggyCommitMessages(splitted_messages)
    


def processMessages(comm_list):
    for comm_mess in comm_list:
        processMessage(comm_mess)

if __name__=='__main__':
    comm_mess_file='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/IaC_Defect_Categ_Revamp/dataset/OSTK_PUPP_COMM_ONLY_DEFE.csv'
    comm_mess_df  = pd.read_csv(comm_mess_file)
    comm_mess_ls  = np.unique ( comm_mess_df['MESSAGE'].tolist() )
    # print comm_mess_df.head()
    processMessages(comm_mess_ls)