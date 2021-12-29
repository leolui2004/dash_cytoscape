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