from pathlib import Path
import re
p=Path(__file__).resolve().parent
s=(p/'evidence/before-cover-v5/index.html.txt').read_text()
s,n=re.subn(r'<img class="cover-presenter"[^>]*>','',s,count=1)
assert n==1
s=s.replace('#cover-v3 .cover-tech-bg{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}', '#cover-v3 .cover-tech-bg{position:absolute;left:10px;top:-430px;width:1600px;height:2844px;max-width:none;object-fit:cover}')
(p/'index.html').write_text(s)
print('Cover has no presenter; preserved v4 body. Do not overwrite manual edits.')
