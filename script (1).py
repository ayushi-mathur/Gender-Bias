import json
import requests
from bs4 import BeautifulSoup
import lxml
import urllib.parse as urlparse

# Page URLs <<<
page_urls = [
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=_Ys2AOPP__8J&astart=10",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=xA4ZAGTm__8J&astart=20",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=Pkx_AITs__8J&astart=30",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=dnIgAG_x__8J&astart=40",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=GvoeAMb0__8J&astart=50",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=jMdRAFf2__8J&astart=60",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=DGbDALL4__8J&astart=70",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=5TiEAPL5__8J&astart=80",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=AtJ-AGb8__8J&astart=90",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=eAxKADH9__8J&astart=100",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=Eh4qAAP-__8J&astart=110",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=pGx_AIb-__8J&astart=120",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=IYKQALP-__8J&astart=130",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=n4ECAPv-__8J&astart=140",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=5ysaACT___8J&astart=150",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=LtF-AE____8J&astart=160",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=Sxc0AHX___8J&astart=170",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=4hMOAJ____8J&astart=180",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=dHgrALP___8J&astart=190",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=nY4LANH___8J&astart=200",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=tGOCAN7___8J&astart=210",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=4ZoNAOf___8J&astart=220",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=eHVYAO3___8J&astart=230",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=xkhEAPX___8J&astart=240",
    "https://scholar.google.com/citations?view_op=view_org&hl=en&org=17916768844747848345&after_author=uKCEAPn___8J&astart=250",
]
# >>>
final_json = {
    "researchers": []
}

for page in page_urls:

    res = requests.get(page)
    if res.status_code != 200:
        print(f"Error : Page {page} : Code {res.status_code}")
    content = res.content

    soup = BeautifulSoup(content, 'lxml')
    users = soup.find_all('h3', attrs={'class': 'gs_ai_name'})
    users = [user.parent for user in users]

    for user in users:
        user_obj = {}
        link = f'https://scholar.google.com{user.find("a")["href"]}'
        parsed_link = urlparse.urlparse(link)
        user_obj["id"] = urlparse.parse_qs(parsed_link.query)["user"][0]
        user_obj["name"] = user.find("a").text
        user_obj["bio"] = user.find("div", attrs={"class": "gs_ai_aff"}).text
        try:
            user_obj["citations"] = int(user.find("div", attrs={"class": "gs_ai_cby"}).text[9:])
        except ValueError as ve:
            print("Value Error!!", link, user.find("div", attrs={"class": "gs_ai_cby"}).text)
            user_obj["citations"] = int(input())
        user_obj["topics"] = [_.text for _ in user.find_all("a", attrs={'class': "gs_ai_one_int"})]
        final_json["researchers"].append(user_obj)

with open("./iis_researchers.json", "w") as f:
    json.dump(final_json, f, indent=4, sort_keys=True)
