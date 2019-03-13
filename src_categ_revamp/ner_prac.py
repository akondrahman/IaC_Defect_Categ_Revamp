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