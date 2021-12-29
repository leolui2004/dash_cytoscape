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