"""Key generation and bundle verification for signed evidence timelines.

python -m sentinelbrief.evidence keygen --out <new file for the private seed>
python -m sentinelbrief.evidence verify <bundle directory> [--public-key HEX]
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from sentinelbrief.evidence.signing import KEY_FILE_ENV, generate_keypair, verify_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    keygen = commands.add_parser("keygen", help="write a new private seed to a file")
    keygen.add_argument("--out", type=Path, required=True, help="file to create for the seed")
    verify = commands.add_parser("verify", help="verify a signed export bundle")
    verify.add_argument("bundle", type=Path)
    verify.add_argument("--public-key", help="the key you expect, obtained outside the bundle")
    args = parser.parse_args(argv)
    if args.command == "keygen":
        seed, public = generate_keypair()
        try:
            # Exclusive create: never overwrite a key, and never print the seed (terminal and
            # CI logs are kept). Owner-only permissions where the platform supports them.
            descriptor = os.open(args.out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            print(f"Refusing to overwrite {args.out}", file=sys.stderr)
            return 2
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(seed + "\n")
        print(
            f"Private seed written to {args.out}. Keep it secret; set {KEY_FILE_ENV} to its path."
        )
        print(f"Public key (give this to whoever will verify bundles): {public}")
        return 0
    result = verify_bundle(args.bundle, args.public_key)
    print("TRUSTED" if result["trusted"] else "NOT TRUSTED")
    print(result["reason"])
    return 0 if result["trusted"] else 1


if __name__ == "__main__":
    sys.exit(main())
