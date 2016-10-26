from analysis import get_root_preselection
from k3pi_config import get_mode, config
from k3pi_utilities import variables, helpers, parser, get_logger
from k3pi_utilities.variables import m, dtf_m, evt_num
from treesplitter import treesplitter
import root_pandas
import tempfile
import tqdm
from multiprocessing import Pool
import pandas as pd

log = get_logger('download_data')


def download(mode, polarity, year):
    log.info('Getting data for {} {} {}'.format(
        mode, polarity, year))
    mode = get_mode(polarity, year, mode)

    sel = get_root_preselection.get(mode)

    if args.full is False:
        sel += ' && ({} % 20 == 0)'.format(evt_num())

    tempfile.mktemp('.root')

    if args.test:
        mode.files = mode.files[:4]
    chunked = list(helpers.chunks(mode.files, 25))
    length = len(list(chunked))

    for part in mode.head.all_mothers() + mode.head.all_daughters():
        for func in variables.__all__:
            try:
                getattr(variables, func)(part)
            except variables.AccessorUsage:
                pass

    add_vars = {
        'delta_m': '{} - {}'.format(m(mode.head), m(mode.D0)),
        'delta_m_dtf': '{} - {}'.format(dtf_m(mode.head), dtf_m(mode.D0))
    }

    def run_splitter(fns):
        temp_file = tempfile.mktemp('.root')
        treesplitter(files=fns, treename=mode.get_tree_name(), output=temp_file,
                     variables=list(variables.all_ever_used), selection=sel,
                     addvariables=add_vars)
        return temp_file

    pool = Pool(processes=4)
    temp_files = []
    for r in tqdm.tqdm(pool.imap_unordered(run_splitter, chunked, chunksize=1),
                       leave=True, total=length, smoothing=0):
        temp_files.append(r)

    log.info('Created {} temporary files.'.format(len(temp_files)))

    with pd.get_store(config.data_store) as store:
        try:
            store.remove(mode.get_tree_name())
            log.info('Removing already existing data at {}'.format(
                mode.get_tree_name()))
        except KeyError:
            log.info('No previous data found. Nothing to delete.')

    df_gen = root_pandas.read_root(temp_files, mode.get_tree_name(),
                                   chunksize=[50000, 100][args.test])
    for df in df_gen:
        log.info('Adding {} events of {} to store {}.'.format(
            len(df), mode.get_tree_name(), config.data_store))
        df.to_hdf(config.data_store, mode.get_tree_name(),
                  mode='a', format='t', append=True)

if __name__ == '__main__':
    args = parser.create_parser()
    download(args.mode, args.polarity, args.year)
