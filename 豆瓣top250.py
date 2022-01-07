import re
import requests
import pandas as pd

def main():
    start = 0
    end = 226
    url = "https://movie.douban.com/top250"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "Cookie": "ll=\"118162\"; bid=c2bkZ7TaLec; _vwo_uuid_v2=DC5C916AA5572C3E5DD6B07A51518C087|a69eb6a26677938cc3358c899fd27b10; __gads=ID=08d55e6dd0086437-22c4c744aecc0084:T=1634532823:RT=1634532823:S=ALNI_Mau-tqjKa85xDN2VHQqOJu_jJ0rhg; ct=y; _ga=GA1.2.1323327205.1634532769; dbcl2=\"166106316:3pJyJG6Ieuo\"; ck=WvZB; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1635606595%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_id.100001.4cf6=3e88e6eed67e7f28.1634532770.3.1635606595.1634630968.; _pk_ses.100001.4cf6=*; __utma=30149280.1323327205.1634532769.1634630954.1635606595.3; __utmb=30149280.0.10.1635606595; __utmc=30149280; __utmz=30149280.1635606595.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.346192371.1634532770.1634532770.1635606595.2; __utmb=223695111.0.10.1635606595; __utmc=223695111; __utmz=223695111.1635606595.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0",
        "Referer": "https://accounts.douban.com/",
    }
    # params = {
    #     "start": first,
    #     "filter": ""
    # }
    # resp = requests.get(url,headers=headers,params=params)
    # page_content = resp.text
    # 解析数据
    obj = re.compile(r'<li>.*?<em class="">(?P<rank>\d{1,}).*?'
                     r'<span class="title">(?P<name>\w+)</span>.*?'
                     r'<p class="">.*?(?P<director>导演.*?)((&nbsp;)+|...<br>).*?(?P<year>\d+)(&nbsp;)+.*?'
                     r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                     r'<span>(?P<evaluation>.*?)</span>',re.S)

    alldata = []
    for first in range(start,end,25):
        params = {
            "start": first,
            "filter": ""
        }
        resp = requests.get(url, headers=headers, params=params)
        page_content = resp.text
        result = obj.finditer(page_content)

        for it in result :
            # print(it.group("rank"),it.group("name"),it.group("director"),it.group("year"),it.group("score"),it.group("evaluation"))
            dic = it.groupdict()
            alldata.append(dic)
    df = pd.DataFrame(alldata)
    df.columns = ['排名', '电影', '导演', '上映年份', '评分', '评价人数']
    df.drop_duplicates(inplace=True)  # 去除重复
    df.to_csv("data.csv",mode="w",index=False) # 不加index = false 会多一列
    resp.close()




if __name__ == '__main__':
    main()
