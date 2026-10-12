#!/usr/bin/env python3
"""Validate that an artifact claims only outcomes supported by its preflight receipt."""
import json,sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else 'p6-verifier-results');r=json.loads((p/'runner_capability.json').read_text())
assert r['runner_connected']==r['hello_world_pass']
assert r['swegym_image_pulled'] is False and r['swegym_tests_executed'] is False
assert (p/'output_manifest.json').is_file()
print('PREFLIGHT_EVIDENCE_VALID; SWE_GYM_NOT_RUN')
