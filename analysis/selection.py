from k3pi_utilities.variables import (eta, probnnk, probnnpi, p, m, dtf_dm,
                                      probnnmu, dtf_chi2, probnnp, pt, vchi2,
                                      maxdoca)
from k3pi_utilities.variables import ipchi2, probnnghost
from k3pi_utilities.selective_load import selective_load
from k3pi_utilities.decorator_utils import pop_arg
from k3pi_utilities.buffer import buffer_load
from k3pi_utilities.debugging import call_debug
from k3pi_utilities import parser
from k3pi_config.modes import gcm, MODE
from k3pi_config import config
import numpy as np


@pop_arg(selective_load, allow_for=[None, 'mc'])
@call_debug
def _apply_pid_cut(df, min_pi_nnpi=0.3, max_pi_nnk=0.7,
                   min_k_nnk=0.3, max_k_nnpi=0.7):
    ret = True
    for kaon in gcm().head.all_pid(config.kaon):
        ret &= (df[probnnk(kaon)] > min_k_nnk) & (df[probnnpi(kaon)] < max_k_nnpi)  # NOQA
    for pion in gcm().head.all_pid(config.pion):
        ret &= (df[probnnpi(pion)] > min_pi_nnpi) & (df[probnnk(pion)] < max_pi_nnk)  # NOQA

    return ret


@pop_arg(selective_load, allow_for=[None, 'mc'])
@call_debug
def _apply_slow_pion_cut(df, min_spi_nnpi=0.3, max_spi_nnk=0.7,
                         max_spi_nnghost=0.05, max_spi_nnp=0.05):
    ret = True
    ret = (df[probnnghost(gcm().Pislow)] < max_spi_nnghost)
    ret &= (df[probnnpi(gcm().Pislow)] > min_spi_nnpi)
    ret &= (df[probnnk(gcm().Pislow)] < max_spi_nnk)
    ret &= (df[probnnmu(gcm().Pislow)] < 0.1)
    ret &= (df[probnnp(gcm().Pislow)] < max_spi_nnp)

    return ret


@buffer_load
def pid_selection():
    return _apply_pid_cut()


@buffer_load
@pop_arg(selective_load, allow_for=[None, 'mc'])
@call_debug
def pid_fiducial_selection(df):
    ret = True
    for part in gcm().D0.all_daughters():
        ret &= (df[p(part)] >= 3000.)
        ret &= (df[p(part)] < 100000.)
        ret &= (df[eta(part)] >= 2.)
        ret &= (df[eta(part)] < 5.)

    return ret


@buffer_load
@pop_arg(selective_load, allow_for=[None, 'mc'])
@call_debug
def mass_fiducial_selection(df):
    ret = True
    ret &= (df[m(gcm().D0)] >= 1810.)
    ret &= (df[m(gcm().D0)] < 1920.)
    ret &= (df[dtf_dm()] >= 140.5)
    ret &= (df[dtf_dm()] < 160.5)

    return ret


@buffer_load
@pop_arg(selective_load, allow_for=[None, 'mc'])
@call_debug
def remove_secondary(df):
    return np.log(df[ipchi2(gcm().D0)]) < 1.


@buffer_load
@pop_arg(selective_load, allow_for=[None, 'mc'])
@call_debug
def d0_selection(df):
    ret = True
    ret &= np.log(df[ipchi2(gcm().D0)]) < 1.
    ret &= df[pt(gcm().D0)] > 4000.
    ret &= df[vchi2(gcm().D0)] < 4.
    ret &= df[maxdoca(gcm().D0)] < .2
    return ret


@buffer_load
def slow_pion():
    return _apply_slow_pion_cut()


@buffer_load
@selective_load
@call_debug
def dtf_cuts(df):
    ret = (df[dtf_chi2(gcm().head)] < 60.)
    return ret


@buffer_load
@call_debug
def full_selection():
    sel = pid_selection()
    sel &= pid_fiducial_selection()
    sel &= mass_fiducial_selection()
    sel &= d0_selection()
    sel &= slow_pion()
    # sel &= dtf_cuts()
    return sel


@buffer_load
@selective_load
@call_debug
def mass_signal_region(df):
    ret = True
    ret &= np.abs(df[m(gcm().D0)] - config.PDG_MASSES['D0']) < 20.
    ret &= np.abs(df[dtf_dm()] - config.PDG_MASSES['delta']) < 0.5
    return ret


@buffer_load
@selective_load
@call_debug
def mass_sideband_region(df):
    ret = True
    ret &= np.abs(df[m(gcm().D0)] - config.PDG_MASSES['D0']) > 30.
    ret &= np.abs(df[dtf_dm()] - config.PDG_MASSES['delta']) > 2.0
    return ret


if __name__ == '__main__':
    import sys
    args = parser.create_parser()

    if args.selections is None:
        sels = [
            'pid_selection',
            'pid_fiducial_selection',
            'mass_fiducial_selection',
            'remove_secondary',
            'd0_selection',
            'slow_pion',
            'mass_signal_region',
            'mass_sideband_region',
            'dtf_cuts',
            'full_selection',
        ]
    else:
        sels = args.selections

    with MODE(args.polarity, args.year, args.mode):
        for sel in sels:
            getattr(sys.modules[__name__], sel)(use_buffered=False)
