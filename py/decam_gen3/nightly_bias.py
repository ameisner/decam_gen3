#!/usr/bin/env python

"""
decam_gen3.nightly_bias
========================
Pipeline driver for preparing creation of a master bias for a given night.
"""

import argparse

if __name__ == "__main__":
    descr = 'prepare creation of a master bias for a given night'

    parser = argparse.ArgumentParser(description=descr)

    parser.add_argument('caldat', type=str, nargs=1,
                        help="observing night in YYYY-MM-DD format")

    parser.add_argument('--repo_name', default='repo', type=str,
                        help="Butler repository name")

    parser.add_argument('--script_name', default='launch.sh', type=str,
                        help="output name for bias creation script")

    args = parser.parse_args()
