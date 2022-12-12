from multiprocessing.sharedctypes import Value
import requests
from bs4 import BeautifulSoup
import lxml
import urllib.parse as urlparse
import json

final_users = {}
user_ids = None
with open("./iis_researchers.json", "r") as f:
    r = json.load(f)["researchers"]
    user_ids = r
new_dic={
    "papers": {}
}
    
for suyash in user_ids:
    user_id = suyash["id"]
    curr=0
    cont_flag=True
    prev_end=""
    papers_arr=[]
    while cont_flag:
        url = f"https://scholar.google.com/citations?user={user_id}&hl=en&cstart={curr}&pagesize=100"
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error : Page {curr} : Code {res.status_code}")
        content = res.content

        soup = BeautifulSoup(content, 'lxml')
        show_more_button = soup.find("button", attrs={'id': 'gsc_bpf_more'})
        print(show_more_button)
        papers = soup.find_all('tr', attrs={'class': 'gsc_a_tr'})
        # papers = [user.parent for user in papers]
        for user in papers:
            cd = user.find("a", attrs={"class": "gsc_a_at"})
        if cd is None or cd.text == prev_end:
            break
        papers = soup.find_all('tr', attrs={'class': 'gsc_a_tr'})
        
        for user in papers:
            paper_obj = {}
            paper_obj["name"] = user.find("a", attrs={"class": "gsc_a_at"}).text
            paper_obj["citations"] = user.find("td", attrs={"class": "gsc_a_c"}).text
            a = user.find_all("div", attrs={"class": "gs_gray"})
            paper_obj["authors"]=a[0].text
            paper_obj["conference"] = a[1].text
            paper_obj["year"] = user.find("td", attrs={"class": "gsc_a_y"}).find("span").text
            print(paper_obj)
            papers_arr.append(paper_obj)
        curr+=100
        prev_end=cd
    new_dic["papers"][suyash["id"]]=papers_arr

with open("./iis_papers.json", "w") as f:
    json.dump(new_dic, f)
