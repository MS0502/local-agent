#!/usr/bin/env python3
"""Hash preflight evidence files into output_manifest.json."""
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else 'p6-verifier-results');root.mkdir(parents=True,exist_ok=True)
files=[]
for f in sorted(root.rglob('*')):
 if f.is_file() and f.name!='output_manifest.json':
  b=f.read_bytes();files.append({'path':f.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(root/'output_manifest.json').write_text(json.dumps({'schema':'ada-p6-output-manifest-v1','file_count':len(files),'files':files},indent=2)+'\n',encoding='utf-8')
