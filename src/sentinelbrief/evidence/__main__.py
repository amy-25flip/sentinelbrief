"""Key generation and bundle verification for signed evidence timelines.

python -m sentinelbrief.evidence keygen
python -m sentinelbrief.evidence verify <bundle directory> [--public-key HEX]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sentinelbrief.evidence.signing import KEY_ENV, generate_keypair, verify_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("keygen", help="print a new private seed and its public key")
    verify = commands.add_parser("verify", help="verify a signed export bundle")
    verify.add_argument("bundle", type=Path)
    verify.add_argument("--public-key", help="the key you expect, obtained outside the bundle")
    args = parser.parse_args(argv)
    if args.command == "keygen":
        seed, public = generate_keypair()
        print(f"Private seed (keep secret; set {KEY_ENV} to this value): {seed}")
        print(f"Public key (give this to whoever will verify bundles):  {public}")
        return 0
    result = verify_bundle(args.bundle, args.public_key)
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] and result["key_pinned"] else 1


if __name__ == "__main__":
    sys.exit(main())
