# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib
P=Path(__file__).resolve().parent;Q=P/'qa/visual-v7'
h=(P/'index.html').read_text()
assert hashlib.sha256(h.encode()).hexdigest()=='8f8476c639971a0ce579fd9ce82fc4a2608c0f52ec5ebc33fdb8fc84b1a0d298'
old='anim("chapter-box",[{transform:"scaleX(0)",opacity:0},{transform:"scaleX(1)",opacity:1}],31.25,.4);'
new='anim("chapter-box",[{opacity:0},{opacity:1}],31.25,.4);'
assert h.count(old)==1
(Q/'index-first-render.html.txt').write_text(h)
h=h.replace(old,new)
(P/'index.html').write_text(h)
(Q/'index-v7.html.txt').write_text(h)
print('Only chapter highlight changed from compressing rectangle to fixed-position opacity fade')
