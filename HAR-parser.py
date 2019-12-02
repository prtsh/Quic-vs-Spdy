import os, sys

#parse the HAR file of a given configuration and 
#spit out the list of PLT (time)
#min PLT, max PLT, avg PLT
#Could be used to plot CDF of the plt

'''
    parse_jq = r'jq -r \'.log.pages[] | [.pageTimings.onLoad, .title]|@tsv\' {}'.format(harfile)
    print(parse_jq)
'''



