import json
from guess_indian_gender import IndianGenderPredictor
f=open("./iis_papers.json")
f=json.load(f)
i = IndianGenderPredictor()
f=f['papers']
m=0
fe=0
for user_id in f:
    papers = f[user_id]
    for paper in papers:
        # print(p)
        author = paper["authors"].split(",")[0]
        g=i.predict(name=author)
        if g=="male":
            m+=1
        else:
            fe+=1
print(m)
print(fe)
