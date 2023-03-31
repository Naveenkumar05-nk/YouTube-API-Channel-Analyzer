#!/usr/bin/env python
# coding: utf-8

# # Project - YouTube API Channel Analyzer

# ### Import Libraries

# In[135]:


import requests
import pandas as pd
import time
from matplotlib import pyplot as plt
     


# ### Credentials to connect with YouTube v3 API

# In[136]:


API_KEY = "" #YouTube API v3 API KEY
CHANNEL_ID = "" #YouTube channel id


# ### Function to get the video details

# In[137]:


def get_video_details(video_id):

    #collecting view, like, dislike, comment counts
    url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+API_KEY
    response_video_stats = requests.get(url_video_stats).json()

    view_count = response_video_stats['items'][0]['statistics']['viewCount']
    like_count = response_video_stats['items'][0]['statistics']['likeCount']
    comment_count = response_video_stats['items'][0]['statistics']['commentCount']

    return view_count, like_count, comment_count


# ### Function to get the channel videos

# In[138]:


def get_videos(df):
    pageToken = ""
    while 1:
        url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000&"+pageToken

        response = requests.get(url).json()
        #print(response)
        time.sleep(1) #give it a second before starting the for loop
        for video in response['items']:
            if video['id']['kind'] == "youtube#video":
                video_id = video['id']['videoId']
                video_title = video['snippet']['title']
                video_title = str(video_title).replace("&","").replace("#39;","'").replace("quot;","'")
                upload_date = video['snippet']['publishedAt']
                upload_date = str(upload_date).split("T")[0]
                view_count, like_count, comment_count = get_video_details(video_id)

                df = df.append({'video_id':video_id,'video_title':video_title,
                                "upload_date":upload_date,"view_count":view_count,
                                "like_count":like_count,"comment_count":comment_count},ignore_index=True)
        try:
            if response['nextPageToken'] != None: #if none, it means it reached the last page and break out of it
                pageToken = "pageToken=" + response['nextPageToken']

        except:
            break


    return df


# ### Main Function

# In[139]:


if __name__=="__main__":

    df = pd.DataFrame(columns=["video_id","video_title","upload_date","view_count","like_count","comment_count"]) 

    df = get_videos(df)
     


# ### Display DataFrame

# In[140]:


display(df)


# ### Top 5 most viewed videos with upload dates

# In[141]:


Top_5_most_viewed_videos = df.sort_values(by=['view_count']).head(5)


# In[142]:


Top_5_most_viewed_videos


# In[143]:


#Changing the datatypes of the values to plot the graph
Top_5_most_viewed_videos['view_count']= Top_5_most_viewed_videos['view_count'].astype(int)
Top_5_most_viewed_videos['upload_date']= Top_5_most_viewed_videos['upload_date'].astype(str)
Top_5_most_viewed_videos.plot(x='upload_date', y='view_count',kind="bar")


# ### Least 5 viewed videos with upload dates

# In[144]:


df['view_count'] = df['view_count'].astype(int)
Least_5_viewed_videos= df.nsmallest(5, 'view_count')


# In[145]:


Least_5_viewed_videos


# In[146]:


#Changing the datatypes of the values to plot the graph
Least_5_viewed_videos['view_count']= Least_5_viewed_videos['view_count'].astype(int)
Least_5_viewed_videos['upload_date']= Least_5_viewed_videos['upload_date'].astype(str)
Least_5_viewed_videos.plot(x='upload_date', y='view_count',kind="bar")

