from pathlib import Path
import re
p=Path(__file__).resolve().parent
s=(p/'evidence/before-cover-v4/index.html.txt').read_text()
s=s.replace('</style>',(p/'data/cover-v4.css').read_text()+'</style>',1)
s,n=re.subn(r'<section id="cover-v3".*?</section>',(p/'data/cover-v4.html.txt').read_text(),s,count=1)
assert n==1
(p/'index.html').write_text(s)
print('Only cover replaced from preserved v3; do not run over manual Studio edits.')
