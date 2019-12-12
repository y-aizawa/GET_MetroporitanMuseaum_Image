#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib
import json
import random
import os


# In[2]:


def get_objectIDs():
    # Web APIのURLを定義
    url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects'
    
    # URLを開く
    objects = urllib.request.urlopen(url)
    # webAPIからのJSONを取得
    response = objects.read()
    # JSONをPythonで使える形式にする
    response_json = json.loads(response)
    # ObjectIDsを取得
    objectIDs = response_json["objectIDs"]
    
    return objectIDs


# In[3]:


def get_object(objectIDs):
    # ObjectIDのリストからランダムで一つを選択
    objectID = random.choice(objectIDs)

    # Web APIのURLを定義
    url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(objectID)

    # URLを開く
    objects = urllib.request.urlopen(url)
    # webAPIからのJSONを取得
    response = objects.read()
    # JSONをPythonで使える形式にする
    response_json = json.loads(response)
    
    return response_json


# In[4]:


def get_publicObject(objectIDs):
    while True:
        # ランダムで一つのオブジェクトを取得
        object_ = get_object(objectIDs)

        # パブリックドメインだった場合レスポンス
        if object_["isPublicDomain"] == True:
            return object_


# In[5]:


def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
            local_file.write(web_file.read())
    except urllib.error.URLError as e:
        print(e)


# In[6]:


if __name__ == '__main__':
    # ObjectIDのリストを取得
    objectIDs = get_objectIDs()

    # ランダムで一つのパブリックドメインオブジェクトを取得
    object_ = get_publicObject(objectIDs)

    # イメージURLを取得
    image_url = object_["primaryImage"]

    # イメージ名を取得
    image_name = os.path.basename(image_url)

    # イメージをダウンロード
    urllib.request.urlretrieve(image_url, "./" + image_name)

