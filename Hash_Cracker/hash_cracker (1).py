#!/usr/bin/env python3
"""
Dictionary-based Hash Cracker with Salt Support

Usage:
    python3 hash_cracker.py <hashes_file> <wordlist_file> [--salt SALT]

Example:
    python3 hash_cracker.py hashes.txt wordlist.txt --salt "mysalt"
"""

import hashlib
import sys

# --- Parse Arguments ---
if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <hashes_file> <wordlist_file> [--salt SALT]")
    sys.exit(1)

hash_file = sys.argv[1]
wordlist_file = sys.argv[2]

# Optional salt argument
salt = ""
if "--salt" in sys.argv:
    try:
        salt_index = sys.argv.index("--salt") + 1
        salt = sys.argv[salt_index]
        print(f"[+] Using salt: '{salt}'")
    except IndexError:
        print("Error: --salt provided but no value given")
        sys.exit(1)

# --- Read Target Hashes ---
try:
    with open(hash_file, 'r') as hf:
        target_hashes = {line.strip().lower() for line in hf if line.strip()}
except Exception as e:
    print(f"Error reading hashes file: {e}")
    sys.exit(1)

# Group hashes by length
hashes_by_length = {}
for h in target_hashes:
    length = len(h)
    hashes_by_length.setdefault(length, set()).add(h)

# Supported Algorithms
algorithms = {
    'MD5':    hashlib.md5,
    'SHA1':   hashlib.sha1,
    'SHA224': hashlib.sha224,
    'SHA256': hashlib.sha256,
    'SHA384': hashlib.sha384,
    'SHA512': hashlib.sha512
}

# Precompute hex digest lengths
algo_lengths = { name: len(func().hexdigest()) for name, func in algorithms.items() }

found_any = False

# --- Crack Loop ---
try:
    with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as wf:
        for line in wf:
            word = line.strip()
            if not word:
                continue

            # Add salt in front of the password candidate
            candidate = (salt + word).encode('utf-8')

            for name, func in algorithms.items():
                digest_len = algo_lengths[name]

                if digest_len not in hashes_by_length:
                    continue

                hashed = func(candidate).hexdigest()

                if hashed in hashes_by_length[digest_len]:
                    print(f"[MATCH] Word: '{word}' | With Salt: '{salt}' "
                          f"| Algorithm: {name} | Hash: {hashed}")
                    found_any = True
except Exception as e:
    print(f"Error reading wordlist file: {e}")
    sys.exit(1)

if not found_any:
    print("No matching hashes found.")
