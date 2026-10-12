# P6 isolated verifier bootstrap

This repository contains public SWE-Gym task identifiers and test-patch hashes only. No ADA source, private logs, model weights, credentials, or test patch contents are included.

The manually dispatched `ADA P6 External Verifier` workflow is preflight-only. It records OS/architecture, CPU, RAM, disk, Docker CLI/daemon status, and runs Docker `hello-world` with resource/capability restrictions. It does not download SWE-Gym images or execute benchmark code. The 120 GiB free-disk mark is a storage qualification gate, not a claim that a task image fits.

After preflight, the exact task image references/digests, compatible SWE-Bench-Fork revision and verifier commands must be pinned before any SWE-Gym task execution. `run_external_verifier.py` fails closed pending those inputs. Verify test patches against the hashes in `task_manifest.json`; test patches are not solution patches.
