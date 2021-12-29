'''
https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-followers-ids
Ai, micaholic1981
あいみょん, aimyonGtter
石川さゆり, なし
Awesome City Club, CcAwesome
上白石萌音, mone_tohoent
坂本冬美, Fuyumi_staff
櫻坂46, sakurazaka46
天童よしみ, なし
東京事変, nekoyanagi_line
NiziU, NiziU__official
乃木坂46, nogizaka46
Perfume, Perfume_Staff
BiSH, BiSHidol
日向坂46, hinatazaka46
松田聖子, なし
MISIA, MISIA
水森かおり, mizumyoutube
milet, milet_music
millennium parade x Belle（中村佳穂）, なし (mllnnmprd, KIKI_526)
薬師丸ひろ子, なし
YOASOBI, YOASOBI_staff
LiSA, LiSA_OLiVE
'''

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