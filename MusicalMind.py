#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
import numpy as np


# In[26]:


url = 'https://raw.githubusercontent.com/SanskarJadhav/musicalmind/main/musicdata.csv'
df = pd.read_csv(url)


# In[27]:


df.rename(columns = {'spotify_track_album':'Album',
                    'spotify_genre':'Genre',
                    'popularity':'Popularity',
                    'spotify_track_id':'Audio Track'}, inplace = True)


# In[28]:


def make_clickable(val):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val, val)


# In[29]:


def get_recommendations(df, song_name, artist_name, amount):
    distances = []
    #choosing the data for our song
    row = df.loc[(df.Song == song_name) & (df.Performer == artist_name)].head(1)
    song = row.values[0]
    ind = row.index[0]
    #dropping the data with our song
    res_data = df.drop(ind)
    for r_song in res_data.values:
        dist = 0
        for col in np.arange(len(res_data.columns)):
            #indeces of non-numerical columns
            if col not in [1,2,3,4,5,7,31]:
                #calculating the manhettan distances for each numerical feature
                dist += np.absolute(float(song[col]) - float(r_song[col]))
        distances.append(dist)
    res_data['distance'] = distances
    #sorting our data to be ascending by 'distance' feature
    res_data = res_data.sort_values('distance')
    res_data['Audio Track'] = res_data['Audio Track'].apply(make_clickable)
    columns=['Song', 'Album', 'Performer', 'Genre', 'Popularity', 'Audio Track']
    return res_data[columns][:amount]

def get_song(df, song_name, artist_name):
    pes_data = df.copy()
    pes_data['Audio Track'] = pes_data['Audio Track'].apply(make_clickable)
    return pes_data.loc[(pes_data.Song == song_name) & (pes_data.Performer == artist_name)].head(1)

# In[30]:


import streamlit as st

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://wallpaperaccess.com/full/2774267.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

tk = 0
st.title('MusicalMind: A Music Recommendation System')

col1, col2 = st.columns(2)

#taking song name as input
with col1:
    song_name = st.selectbox('Enter a song: ', set(df['Song']), index=0)
    songid = st.checkbox('Include Audio Track URLs')
    
#taking artist name as input
with col2:
    artist_name = st.selectbox('Enter the artists: ', tuple(df[df['Song']==song_name]['Performer']))
    numrec = st.slider('Number of recommendations', 1, 25, 10)
    if st.button('Submit'):
        tk = 1

if tk == 1:
    st.markdown('Song Details of ' + song_name)
    pre = st.empty()
    predf = get_song(df, song_name, artist_name)
    predf.reset_index(drop=True, inplace = True)
    rec = st.empty()
    recdf = get_recommendations(df, song_name, artist_name, numrec)
    recdf.reset_index(drop=True, inplace=True)
    if songid:
        predf = predf.loc[:,['Song', 'Performer', 'Audio Track']]
        pre = st.write(predf.to_html(escape = False), unsafe_allow_html = True)
        st.markdown('Recommending songs similar to '+ song_name + " by " + artist_name)
        recdf = recdf.loc[:,['Song', 'Performer', 'Audio Track']]
        rec = st.write(recdf.to_html(escape = False), unsafe_allow_html = True)
    else:
        predf = predf.iloc[:,:-1]
        pre = st.dataframe(predf)
        st.markdown('Recommending songs similar to '+ song_name + " by " + artist_name)
        recdf = recdf.iloc[:,:-1]
        rec = st.dataframe(recdf)
        

