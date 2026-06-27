import re,json
bank=open("/sessions/pensive-blissful-allen/mnt/Studying To Shlav Alef/Question Bank - Bologna.md",encoding="utf-8",errors="strict").read()
# sanity: ensure full read (must contain last items)
assert bank.count("**B113.")>=252 and bank.count("**B115.")>=54, ("truncated bank?",bank.count("**B113."),bank.count("**B115."))

# ---- parse QUESTION blocks for B113/B115 ----
qs={}
for m in re.finditer(r'^\*\*(B11[35]\.\d+)\*\* \*\[(Ch11[35]) · (.+?)\]\* (.+?)\n((?:!\[.*?\]\(images/.+?\)\n)?(?:- [A-D]\. .+\n?){4})', bank, re.M):
    qid=m.group(1); chapter=m.group(2); section=m.group(3); stem=m.group(4); rest=m.group(5)
    img=re.search(r'!\[(.*?)\]\(images/(B11[35]-\d+\.jpg)\)',rest)
    opts=dict(re.findall(r'^- ([A-D])\. (.+)$',rest,re.M))
    qs[qid]={'chapter':chapter,'section':section,'stem':stem,'options':opts,
             'image':('images/'+img.group(2)) if img else None,'imgcap':(img.group(1) if img else None)}
# ---- parse ANSWER blocks ----
ans={}
# split on answer headers
parts=re.split(r'^\*\*(B11[35]\.\d+) — ([A-D])\.\*\* ',bank,flags=re.M)
for i in range(1,len(parts),3):
    qid=parts[i]; letter=parts[i+1]; body=parts[i+2]
    para=body.split('\n',1)[0]
    mm=re.match(r'(.*?)\s*🔑\s*(.*?)\s*📖\s*(.*)',para)
    if not mm:  # safety
        continue
    exp=mm.group(1).strip(); hy=mm.group(2).strip(); src=re.sub(r'\s*\[[a-z]+\]\s*$','',mm.group(3).strip())
    # exptable: contiguous table lines right after the para
    after=body.split('\n')[1:]
    tbl=[]
    for ln in after:
        if ln.startswith('|') and ln.rstrip().endswith('|'):
            cells=[c.strip() for c in ln.strip().strip('|').split('|')]
            if all(set(c)<=set('-: ') for c in cells): continue
            tbl.append(cells)
        elif ln.strip()=='' and not tbl:
            continue
        else:
            break
    ans[qid]={'answer':letter,'exp':exp,'hy':hy,'src':src,'exptable':tbl}

# build entries for all B113/B115 ids that have both Q and A
ids=sorted(set(qs)&set(ans), key=lambda x:(x[:4],int(x.split('.')[1])))
built={}
for qid in ids:
    q=qs[qid]; a=ans[qid]
    chnum=q['chapter'][2:]
    chname='Melanoma' if chnum=='113' else 'Neurofibroma & Merkel Cell Carcinoma'
    e={'id':qid,'chapter':q['chapter'],'section':q['section'],'stem':q['stem'],'options':q['options'],
       'answer':a['answer'],'exp':a['exp'],'hy':a['hy'],'src':a['src'],'book':'Bologna','vol':'',
       'chnum':chnum,'chname':chname}
    if q['image']: e['image']=q['image']; e['imgcap']=q['imgcap'] or ''
    if a['exptable']: e['exptable']=a['exptable']
    built[qid]=e
print('parsed B113:',sum(1 for k in built if k.startswith('B113')),'B115:',sum(1 for k in built if k.startswith('B115')))
# validate
bad=[k for k,e in built.items() if len(e['options'])!=4 or e['answer'] not in e['options'] or not e['exp'] or not e['hy'] or not e['src']]
print('invalid:',bad)
json.dump(built,open('built.json','w',encoding='utf-8'),ensure_ascii=False)
