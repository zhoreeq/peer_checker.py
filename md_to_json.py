#!/usr/bin/env python3
import re
import os
import sys
import logging
import json
from datetime import datetime

PEER_REGEX = re.compile(r"`(tcp|tls)://([a-z0-9\.\-\:\[\]]+):([0-9]+)`")

def get_peers(data_dir):
    """Scan repository directory for peers"""
    assert os.path.exists(os.path.join(data_dir, "README.md")), "Invalid path"
    result = {}
    ALL_REGIONS = [d for d in os.listdir(data_dir) if \
            os.path.isdir(os.path.join(data_dir, d)) and \
            not d in [".git", "other"]]

    for region in ALL_REGIONS:
        result[region] = {}
        for country in [f for f in os.listdir(os.path.join(data_dir, region)) if \
                f.endswith(".md")]:
            result[region][country] = []

            cfile = os.path.join(data_dir, region, country)
            if os.path.exists(cfile):
                with open(cfile) as f:
                    for p in PEER_REGEX.findall(f.read()):
                        result[region][country].append("{}://{}:{}".format(*p))

    return result


def print_usage():
    print("Usage: {} [path to public-peers repository on a disk]".format(sys.argv[0]))
    print("I.e.:  {} ~/src/yggdrasil-network/public-peers".format(sys.argv[0]))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        data_dir = sys.argv[1]
    else:
        print_usage()
        sys.exit()

    try:
        peers = get_peers(data_dir)
    except:
        print("Can't find peers in a directory: {}".format(data_dir))
        print_usage()
        sys.exit()

    result = {"date":datetime.utcnow().strftime("%c"), "data":peers}
    print(json.dumps(peers, sort_keys=True, indent=4))
