from __future__ import print_function
from k3pi_utilities import parser, get_logger
from k3pi_config import get_mode, config
from itertools import product
import root_pandas
import ROOT

log = get_logger('luminosity')


def get_luminosity(mode, polarity, year):
    mode = get_mode(polarity, year, mode)

    # For a yet to be determined reason, some files do not contain a LumiTuple
    # so sort those ones out
    infiles = []
    for f in mode.files:
        fl = ROOT.TFile.Open(f)
        if fl.Get('GetIntegratedLuminosity/LumiTuple'):
            infiles.append(f)
        fl.Close()

    # Get the files and stuff them into a dataframe
    df = root_pandas.read_root(
        infiles, key='GetIntegratedLuminosity/LumiTuple')

    log.info('Luminosity {} {}: {} +- {}'.format(
        year, polarity,
        df.sum().IntegratedLuminosity, df.sum().IntegratedLuminosityErr))


if __name__ == '__main__':
    args = parser.create_parser(log)
    if args.polarity == config.magboth:
        pols = [config.magup, config.magdown]
    else:
        pols = [args.polarity]
    if args.year == 1516:
        years = [2015, 2016]
    else:
        years = [args.year]
    for p, y in product(pols, years):
        get_luminosity(args.mode, p, y)
