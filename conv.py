import json
f=open('./Assgnment-2/data/gdata.json')
f=json.load(f)
amul_users = f['users']

suyash_data = open('./Assgnment-2/selected_ids.json', 'r')
suyash_data=json.load(suyash_data)
suyash_data=suyash_data['data']
suyash_users=['priyankachopra']
for item in suyash_data:
    suyash_users.append(item['username'])

amul_edges = f['edges']
suyash_edges=[]
for edge in amul_edges:
    idx1=amul_users.index(edge[0])
    idx2=amul_users.index(edge[1])
    suyash_edges.append((suyash_users[idx1],suyash_users[idx2]))
print(suyash_users)
print(suyash_edges)