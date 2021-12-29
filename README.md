![image](https://github.com/leolui2004/dash_cytoscape/blob/main/pic/m3r1.png)

# Dash Cytoscape to Visualize Relationship between Twitter Accounts

My tenth project on github. An experiment using Cytoscape on Dash to show the network relationships of Twitter followers of some famous artists in Japan, as to analyze the common interests of fans. Please notice that it is a try on cytoscape and a simple demonstration which is not a precise analytical project.

Feel free to provide comments, I just started learning Python last year and I am now concentrating on data analysis, visualization and deep learning applications.

## Simple Introduction

### Goals and Usages

Traditional graphs cannot represent the difficult relationship between networks, the most typical example would be users on social networks, and by using network graphs to visualize those relationships, we can simply find out the common interests of users, knowing the relationship between different type of users, or figure out how to reach the target users.

### Dash Cytoscape

Dash Cytoscape is a visualization tool for showing graphs of networks. There are also many tools for Cytoscape but as I am familiar with Dash, Dash also keeps working very hard on providing more and more tools to users, so I just stick to use Dash by my preference.

### Datasource

This time I used 2021 NHK Kohaku Uta Gassen female artists as the analyzing object. excluding those that do not hold a Twitter account, there are a total of 19 Twitter accounts. I will show the process of retrieving the followers of those Twitter accounts and visualize the relationships in the below section.

List of Names and Twitter accounts
Ai, Ai, micaholic1981
Aimyon, あいみょん, aimyonGtter
Sayuri Ishikawa, 石川さゆり, N/A
Awesome City Club, Awesome City Club, CcAwesome
Mone Kamishiraishi, 上白石萌音, mone_tohoent
Fuyumi Sakamoto, 坂本冬美, Fuyumi_staff
Sakurazaka46, 櫻坂46, sakurazaka46
Yoshimi Tendo, 天童よしみ, N/A
Tokyo Jihen, 東京事変, nekoyanagi_line
NiziU, NiziU, NiziU__official
Nogizaka46, 乃木坂46, nogizaka46
Perfume, Perfume, Perfume_Staff
Bish, BiSH, BiSHidol
Hinatazaka46, 日向坂46, hinatazaka46
Seiko Matsuda, 松田聖子, N/A
Misia, MISIA, MISIA
Kaori Mizumori, 水森かおり, mizumyoutube
Milet, milet, milet_music
Millennium Parade, millennium parade, mllnnmprd
Belle, Belle（中村佳穂）, KIKI_526
Hiroko Yakushimaru, 薬師丸ひろ子, N/A
Yoasobi, YOASOBI, YOASOBI_staff
Lisa, LiSA, LiSA_OLiVE

## Process

### Retrieving Twitter Followers

I have used Twitter API (https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-followers-ids) to get the follower list for each Twitter accounts. As some Twitter accounts got over 1M followers, I have spent 1-2 days retrieving all follower lists. All follower lists are saved as csv with each csv file representing each artist Twitter account. For the sake of privacy information, those followers are represented in Twitter ID instead of name or screen name, however as we are only concerned about the relationship not the followers themselve, this can also save a lot of time (retrieving name of a Twitter account takes much more time).

cytoscape_collect.py
```
from requests_oauthlib import OAuth1Session
import json
import csv
import time

CK = '' # Consumer Key
CS = '' # Consumer Secret
AT = '' # Access Token
AS = '' # Accesss Token Secert
session = OAuth1Session(CK, CS, AT, AS)

def getFollower(screen_name, cursor):
    url = 'https://api.twitter.com/1.1/followers/ids.json'
    res = session.get(url, params = {'screen_name':screen_name, 'cursor':cursor, 'skip_status':1, 'count':5000})
    resText = json.loads(res.text)
    return resText

twitter_dict = {"micaholic1981":"Ai","aimyonGtter":"あいみょん","CcAwesome":"Awesome City Club","mone_tohoent":"上白石萌音",
                "sakurazaka46":"櫻坂46","nekoyanagi_line":"東京事変","NiziU__official":"NiziU","nogizaka46":"乃木坂46","Perfume_Staff":"Perfume",
                "BiSHidol":"BiSH","hinatazaka46":"日向坂46","MISIA":"MISIA","milet_music":"milet",
                "mllnnmprd":"millennium parade","KIKI_526":"Belle（中村佳穂）","YOASOBI_staff":"YOASOBI","LiSA_OLiVE":"LiSA"}

for twitter_account in twitter_dict.keys():
    next_cursor = -1
    follower = twitter_account
    while next_cursor != 0:
        resText = getFollower(follower, next_cursor)
        next_cursor = resText['next_cursor']
        for id in resText['ids']:
            with open(f'raw/{follower}.csv', 'a+', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([id])
        time.sleep(60)
```

### Sampling Followers

As the total follower lists retrieved has over 10M rows, which is infeasible to load on a Dash Cytoscape, thus some kind of sampling is necessary, I have tried few methods and here are the details

Approach 1:
Delete all records which have no relationship (only appear once on all follower lists)
Approach 2:
Take 1% sample from the records (keep 1 record for each 100 records)

For approach 2, that would be an easy job, but for approach 1, there are many methods to achieve, while different methods have different efficiency, here are the methods and also the results

Approach 1 Method 1: For each row of record, find any same appearance in all records
Result: Extremely slow, as you can imagine this is a loop of a loop

Approach 1 Method 2: Set up a SQLite database, for all records, put it (Twitter ID) into the database if it has not been put, otherwise update the frequency of that Twitter ID, after that for each row of record, delete it if the frequency of that Twitter ID is 1 (or keep the rows that only if the frequency of respective Twitter ID is larger than 1)
Result: Slow, SQLite is not good for large IO jobs

Approach 1 Method 3: Just like method 2, but simply use a Python dictionary instead of SQLite database
ResultL Quite fast even if the data is about 10M rows

However, doing only one of the approach is also not enough, as an example, after finishing approach 1, there are 3-4M records remained, or after finishing approach 2, there are 100k records remained, which is still very large for visualization, so the sampling process may need combining the 2 approached together

Sampling process 1: Approach 1 + Approach 2
Result: Some csv still got >30k rows, while some csv just got <10 rows

Sampling process 2: Approach 2 + Approach 1
Result: The maximum rows for one csv is <200, which is just right for visualization

cytoscape_sample.py
```
import csv

twitter_dict = {"micaholic1981":"Ai","aimyonGtter":"あいみょん","CcAwesome":"Awesome City Club","mone_tohoent":"上白石萌音","Fuyumi_staff":"坂本冬美",
                "sakurazaka46":"櫻坂46","nekoyanagi_line":"東京事変","NiziU__official":"NiziU","nogizaka46":"乃木坂46","Perfume_Staff":"Perfume",
                "BiSHidol":"BiSH","hinatazaka46":"日向坂46","MISIA":"MISIA","mizumyoutube":"水森かおり","milet_music":"milet",
                "mllnnmprd":"millennium parade","KIKI_526":"Belle（中村佳穂）","YOASOBI_staff":"YOASOBI","LiSA_OLiVE":"LiSA"}

def sampling():
    for twitter_acct in twitter_dict.keys():
        row_count = 0
        
        with open(f'raw/{twitter_acct}.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                row_count += 1
                if row_count % 100 == 1:
                    with open(f'sample/{twitter_acct}.csv', 'a+', encoding='utf-8', newline='') as file_product:
                        writer = csv.writer(file_product)
                        writer.writerow([row[0]])
    return

acct_dict = sampling()
```

cytoscape_transform.py
```
import csv

twitter_dict = {"micaholic1981":"Ai","aimyonGtter":"あいみょん","CcAwesome":"Awesome City Club","mone_tohoent":"上白石萌音","Fuyumi_staff":"坂本冬美",
                "sakurazaka46":"櫻坂46","nekoyanagi_line":"東京事変","NiziU__official":"NiziU","nogizaka46":"乃木坂46","Perfume_Staff":"Perfume",
                "BiSHidol":"BiSH","hinatazaka46":"日向坂46","MISIA":"MISIA","mizumyoutube":"水森かおり","milet_music":"milet",
                "mllnnmprd":"millennium parade","KIKI_526":"Belle（中村佳穂）","YOASOBI_staff":"YOASOBI","LiSA_OLiVE":"LiSA"}

acct_dict = {}

def get():
    for twitter_acct in twitter_dict.keys():
        print(twitter_acct)
        
        with open(f'sample/{twitter_acct}.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] in acct_dict:
                    acct_dict[row[0]] = acct_dict[row[0]] + 1
                else:
                    acct_dict[row[0]] = 1
    return acct_dict

acct_dict = get()

for twitter_acct in twitter_dict.keys():
    print(twitter_acct)
    
    with open(f'sample/{twitter_acct}.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if acct_dict[row[0]] > 1:
                with open(f'product/{twitter_acct}.csv', 'a+', encoding='utf-8', newline='') as file_product:
                    writer = csv.writer(file_product)
                    writer.writerow([row[0]])
```

### Visulizing Result

After collecting and sampling those data, I used NetworkX to construct a network graph, and then transformed it to a format for Dash Cytoscape (Dash Cytoscape cannot read NetworkX graph directly, there are some related articles on the web discussing this issue).

I have also encountered some bugs when installing pygraphviz on a VM but those can be simply solved by searching solutions on the web.

cytoscape_v2_display.py

## Result

The result image is a nice network graph
![image](https://github.com/leolui2004/dash_cytoscape/blob/main/pic/m2r1.png)

The result clearly shows followers of 46 groups (Sakurazaka 46(櫻坂46), Nogizaka 46(乃木坂46), Hinatazaka 46(日向坂46)) are closely connected together, which should be coincide with our prediction
![image](https://github.com/leolui2004/dash_cytoscape/blob/main/pic/m2r2.png)

![image](https://github.com/leolui2004/dash_cytoscape/blob/main/pic/m2r3.png)
