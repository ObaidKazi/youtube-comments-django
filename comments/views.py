from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import os
import pandas as pd
from itertools import islice
from youtube_comment_downloader import *
import datetime

# Create your views here.

def index(request):
    if request.method=='POST':
        data=request.POST
        url=data.get('url')
        comments_count=data.get('count',30)
        sort_by=data.get('sortby',1)
        comments_count=int(comments_count) if type(comments_count)==str  else comments_count
        sort_by=int(sort_by) if type(sort_by)==str  else sort_by
        if not url:
            return HttpResponse('url not found')
        jsonComments=[]
        downloader = YoutubeCommentDownloader()
        comments = downloader.get_comments_from_url(url,sort_by=sort_by)
        prefixUrl='https://www.youtube.com/channel/'
        
        for comment in islice(comments, comments_count):
            jsonComments.append({
                'Name':comment['author'],
                'Comment':comment['text'],
                'Channel':"=HYPERLINK("+'"'+prefixUrl+comment['channel']+'"'+", "'"'+comment['author']+'"'+")"
                
            })
        date_time = datetime.datetime.now()
        filename=date_time.strftime("%d-%m-%Y_%f")

        pd.DataFrame(jsonComments).to_excel('{}.xlsx'.format(filename))
        # os.system('python comments/youtube_comments.py '+data)
        file_location='{}.xlsx'.format(filename)
        try:    
            with open(file_location, 'rb') as f:
                file_data = f.read()

            # sending response 
            response = HttpResponse(file_data, content_type='application/xlsx')
            response['Content-Disposition'] = 'attachment; filename="comments.xlsx"'

        except IOError:
            # handle file not exist case here
            response = HttpResponseNotFound('<h1>File not exist</h1>')

        return response
        #return FileResponse(open('comments.xlsx', 'rb'), as_attachment=True)
        #return HttpResponse('test')
    else:
        comment_count_list = [i for i in range(0,100,10) if not i==0 ] 
        context = {
            'comment_count_list': comment_count_list
        }
        return render(request,'index.html',context)
