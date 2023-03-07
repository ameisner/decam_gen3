#!/usr/bin/env python

"""
decam_gen3.nightly_bias
========================
Pipeline driver for preparing creation of a master bias for a given night.
"""

import argparse
import decam_reduce.util as util
import os
import glob
import astropy.io.fits as fits

def _patch_raw_headers(flist):
    for f in flist:
        print("PATCHING HEADER FOR " + f)
        util.patch_raw_header(f)

def _get_bias_expnums(flist, as_string=True):

    expids = []
    for f in flist:
        h = fits.getheader(f)
        expids.append(h['EXPNUM'])

    expids.sort() # don't see this as necessary but w/e
    if not as_string:
        return expids
    else:
        expids = tuple(expids)
        return f'BIASEXPS="{expids}"'

def _proc(caldat, repo_name='repo', script_name='launch.sh'):
    """
    prepare creation of a master bias for a given night

    """

    # download the raw bias frames for the night
    #    what if no master bias frames available?
    #    verify the checksums?

    nightsum = util.query_night(caldat)

    result = util.select_raw_zeros(nightsum, n_max=5)

    outdir = 'bias'

    assert(os.path.exists(outdir))
    util.download_images(result, outdir)

    flist = glob.glob(os.path.join(outdir, '*.fz'))
    flist.sort()    
    _patch_raw_headers(flist)
    biasexps = _get_bias_expnums(flist, as_string=True)

    print(biasexps)

    # figure out the exposure ID's of the master bias frames downloaded
    #    either from the API query result or else from the headers
    # patch the biases for e.g., missing HUMIDITY
    # generate the launch script



if __name__ == "__main__":
    descr = 'prepare creation of a master bias for a given night'

    parser = argparse.ArgumentParser(description=descr)

    parser.add_argument('caldat', type=str, nargs=1,
                        help="observing night in YYYY-MM-DD format")

    parser.add_argument('--repo_name', default='repo', type=str,
                        help="Butler repository name")

    parser.add_argument('--script_name', default='launch.sh', type=str,
                        help="output name for bias creation script")

    # make "-j" parallelism level an optional argument as well

    args = parser.parse_args()

    _proc(args.caldat[0], repo_name=args.repo_name,
          script_name=args.script_name)
