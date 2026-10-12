#!/usr/bin/env python3
"""Verify local task-patch files against the public pinned manifest."""
import argparse,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--manifest',default='p6-verifier/task_manifest.json');p.add_argument('--patch-dir',required=True);a=p.parse_args()
m=json.loads(Path(a.manifest).read_text(encoding='utf-8-sig'));root=Path(a.patch_dir);rows=[]
for task in m['tasks']:
 f=root/(task['task_id']+'.test_patch.diff');actual=hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else None
 rows.append({'task_id':task['task_id'],'expected':task['test_patch_sha256'],'actual':actual,'match':actual==task['test_patch_sha256']})
print(json.dumps({'task_count':len(rows),'verified':sum(x['match'] for x in rows),'all_match':all(x['match'] for x in rows),'rows':rows},indent=2));sys.exit(0 if len(rows)==10 and all(x['match'] for x in rows) else 1)
