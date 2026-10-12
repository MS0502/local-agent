#!/usr/bin/env python3
"""Fail-closed gate: external SWE-Gym execution is disabled until provenance is complete."""
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--task-id',required=True);p.add_argument('--image-digest');p.add_argument('--preflight-only',action='store_true');a=p.parse_args()
m=json.load(open('p6-verifier/task_manifest.json',encoding='utf-8-sig'));ids={x['task_id'] for x in m['tasks']}
if a.task_id not in ids: p.error('task-id is not in the pinned ten-task manifest')
if a.preflight_only: print(json.dumps({'status':'PREFLIGHT_ONLY','task_id':a.task_id,'verifier_executed':False}));sys.exit(0)
if not a.image_digest or not a.image_digest.startswith('sha256:'): p.error('exact official image digest required')
sys.exit('STOP: SWE-Gym image mapping, compatible harness revision, and tested command have not been pinned; no external code was run.')
