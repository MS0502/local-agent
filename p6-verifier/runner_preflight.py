#!/usr/bin/env python3
"""Collect runner capabilities and execute only Docker's public hello-world image."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, shutil, subprocess, sys, time
from pathlib import Path

GIB = 1024 ** 3

def run(argv: list[str], log: Path, timeout: int = 120) -> dict:
    started = time.monotonic()
    try:
        proc = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              timeout=timeout, check=False, env={**os.environ, "DOCKER_CLI_HINTS": "false"})
        output = proc.stdout
        code = proc.returncode
    except Exception as exc:
        output, code = f"{type(exc).__name__}: {exc}\n", 127
    log.write_text(output, encoding="utf-8")
    return {"command": argv[0], "exit_code": code, "elapsed_seconds": round(time.monotonic()-started, 3), "log": log.name}

def mem_gib() -> float | None:
    try:
        for line in Path('/proc/meminfo').read_text().splitlines():
            if line.startswith('MemTotal:'):
                return round(int(line.split()[1]) * 1024 / GIB, 2)
    except OSError:
        pass
    return None

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir', default='p6-verifier-results'); a=ap.parse_args()
    out=Path(a.output_dir); out.mkdir(parents=True, exist_ok=True)
    system=run(['uname','-a'],out/'uname.log')
    cli=run(['docker','--version'],out/'docker-version.log')
    info=run(['docker','info'],out/'docker-info.log') if cli['exit_code']==0 else {"exit_code":127,"log":"docker-info.log"}
    hello=run(['docker','run','--pull=always','--rm','--network=none','--cap-drop=ALL','--security-opt=no-new-privileges','--pids-limit=64','--memory=256m','--cpus=0.5','hello-world'],out/'hello-world.log',timeout=180) if info['exit_code']==0 else {"exit_code":127,"log":"hello-world.log"}
    if hello['exit_code']==127 and not (out/'hello-world.log').exists(): (out/'hello-world.log').write_text('Skipped: Docker daemon unavailable.\n',encoding='utf-8')
    root=shutil.disk_usage('/')
    data={"schema":"ada-p6-runner-preflight-v1","event":"workflow_dispatch","runner_provider":"github-actions","runner_environment":os.environ.get("RUNNER_ENVIRONMENT"),"github_run_id":os.environ.get("GITHUB_RUN_ID"),"github_sha":os.environ.get("GITHUB_SHA"),"workflow_ref":os.environ.get("GITHUB_WORKFLOW_REF"),"runner_connected":hello['exit_code']==0,
          "runner_os":platform.platform(),"runner_arch":platform.machine(),"cpu_count":os.cpu_count(),
          "total_ram_gib":mem_gib(),"root_available_disk_gib":round(root.free/GIB,2),
          "docker_cli_status":"PASS" if cli['exit_code']==0 else "FAIL",
          "docker_daemon_status":"PASS" if info['exit_code']==0 else "FAIL",
          "hello_world_pass":hello['exit_code']==0,"hello_world_exit_code":hello['exit_code'],
          "swegym_storage_qualified":root.free >= 120*GIB,
          "swegym_storage_threshold_gib":120,
          "swegym_image_pulled":False,"swegym_tests_executed":False,
          "commands":{"uname":system,"docker_version":cli,"docker_info":info,"hello_world":hello},
          "created_utc":time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    (out/'runner_capability.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    (out/'docker_qualification.json').write_text(json.dumps({"docker_cli":data['docker_cli_status'],"docker_daemon":data['docker_daemon_status'],"hello_world":data['hello_world_pass'],"swegym_storage_qualified":data['swegym_storage_qualified'],"swegym_image_pulled":False},indent=2)+'\n',encoding='utf-8')
    return 0 if data['runner_connected'] else 1
if __name__=='__main__': sys.exit(main())
