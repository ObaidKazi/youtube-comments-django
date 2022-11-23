import pandas as pd
from itertools import islice
from youtube_comment_downloader import *
import sys
jsonComments=[]
downloader = YoutubeCommentDownloader()
comments = downloader.get_comments_from_url(sys.argv[1])

prefixUrl='https://www.youtube.com/channel/'
for comment in islice(comments, 30):
     jsonComments.append({
        'Name':comment['author'],
        'Comment':comment['text'],
        'Channel':"=HYPERLINK("+'"'+prefixUrl+comment['channel']+'"'+", "'"'+comment['author']+'"'+")"
        
     })
pd.DataFrame(jsonComments).to_excel('comments.xlsx')