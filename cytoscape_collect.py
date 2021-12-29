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
