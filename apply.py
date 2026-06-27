import json
live=json.load(open('questions.json'))
built=json.load(open('built.json'))
byid={x['id']:x for x in live}
# 1) refresh B113 exp/hy/src/exptable in place; verify options/answer unchanged
changed=0; mism=[]
for qid,e in built.items():
    if qid.startswith('B113'):
        if qid not in byid: mism.append(('missing',qid)); continue
        cur=byid[qid]
        if cur['options']!=e['options'] or cur['answer']!=e['answer']:
            mism.append(('opt/ans drift',qid)); continue
        cur['exp']=e['exp']; cur['hy']=e['hy']; cur['src']=e['src']
        if 'exptable' in e: cur['exptable']=e['exptable']
        changed+=1
assert not mism, mism
# 2) append B115 (collision check)
add=[e for qid,e in sorted(built.items(),key=lambda kv:int(kv[0].split('.')[1])) if qid.startswith('B115')]
add=[e for e in add]
existing=set(byid)
coll=[e['id'] for e in add if e['id'] in existing]
assert not coll, coll
merged=live+add
json.dump(merged,open('questions.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('B113 refreshed:',changed,'| B115 added:',len(add),'| total:',len(merged))
import collections
print(collections.Counter(x['book'] for x in merged))
# spot check one refreshed B113 exp length grew, and a B115 fig + exptable
b=byid['B113.12']; print('B113.12 exp len:',len(b['exp']))
b115=[x for x in merged if x['id']=='B115.27'][0]; print('B115.27 has image:',b115.get('image'))
b113t=[x for x in merged if x['id']=='B113.82'][0]; print('B113.82 exptable rows:',len(b113t.get('exptable',[])))
