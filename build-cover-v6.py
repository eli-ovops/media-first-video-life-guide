from pathlib import Path
import re
p=Path(__file__).resolve().parent
s=(p/'evidence/before-cover-v6/index.html.txt').read_text()
a=s.index('<section id="cover-v3"');b=s.index('</section>',a)+len('</section>')
c=s[a:b].replace('<h1>人生说明书</h1>','<h1>地球<span class="cover-online-v6">online</span>攻略</h1>')
s=s[:a]+c+s[b:]
s=s.replace('</style>','\n#cover-v3 .cover-top-v4 h1{font-size:142px;letter-spacing:-5px;white-space:nowrap}\n#cover-v3 .cover-online-v6{font-size:126px;letter-spacing:-6px}\n</style>',1)
(p/'index.html').write_text(s)
print('Only title changed from preserved v5; do not overwrite manual edits.')
