import pandas as pd

from pyadlml.constants import ACTIVITY, DEVICE, END_TIME, START_TIME
from pyadlml.dataset._core.activities import correct_activities
from pyadlml.dataset._core.devices import device_boolean_on_states_to_events
from pyadlml.dataset._core.obj import Data
from pyadlml.dataset.io import fetcher, correct_devs, download_from_mega
import os

UCI_ADL_BINARY_URL = 'https://mega.nz/file/AQIgDQJD#oximAQFjexTKwNP3WYzlPnOGew06YSQ2ef85vvWGN94'
UCI_ADL_BINARY_FILENAME = 'uci_adl_binary.zip'
ORD_A = 'OrdonezA'
ORD_B = 'OrdonezB'


@correct_devs   # only correct devices as activities are explicitly handled in function body
@fetcher('uci_adl_binary', download_from_mega, UCI_ADL_BINARY_FILENAME, UCI_ADL_BINARY_URL)
def fetch_uci_adl_binary(subject='OrdonezA', keep_original=True, cache=True,
                         retain_corrections=False, folder_path=None) -> Data:
    """

    Parameters
    ----------
    subject : str of {'OrdonezA', 'OrdonezB'}, default='OrdonezA'
        decides which dataset of the two houses is loaded.
    keep_original : bool, default=True
        Determines whether the original dataset is deleted after downloading
        or kept on the hard drive.
    cache : bool
        Determines whether the data object should be stored as a binary file for quicker access.
        For more information how caching is used refer to the :ref:`user guide <storage>`.
    retain_corrections : bool
        When set to *true* data points that are changed or dropped during preprocessing
        are listed in the respective attributes of the data object.  Fore more information
        about the attributes refer to the :ref:`user guide <error_correction>`.


    Returns
    -------
    data : object
    """
    assert subject in [ORD_A, ORD_B]

    # fix path and Ordonez B activity file
    sub_dev_file = os.path.join(folder_path, '{}_Sensors.txt'.format(subject))
    if subject == ORD_B:
        fix_OrdonezB_ADLS(os.path.join(folder_path, 'OrdonezB_ADLs.txt'))
        sub_act_file = os.path.join(folder_path, '{}_ADLs_corr.txt'.format(subject))
    else:
        sub_act_file = os.path.join(folder_path, '{}_ADLs.txt'.format(subject))

    # load activities and devices
    df_act = _load_activities(sub_act_file)
    df_dev, df_loc = _load_devices(sub_dev_file)
    df_dev = device_boolean_on_states_to_events(df_dev)

    lst_act = df_act[ACTIVITY].unique()
    lst_dev = df_dev[DEVICE].unique()

    data = Data(None, df_dev, activity_list=lst_act, device_list=lst_dev)
    data.df_dev_rooms = df_loc

    # manual activity correction for OrdonezB
    if subject == ORD_B:
        # the activity grooming is often overlapped by sleeping
        # Since grooming is more important make it the dominant activity (opinionated)
        df_act, correction_act = correct_activities(df_act, excepts=['Grooming'], retain_corrections=retain_corrections)

    elif subject == ORD_A:
        # Manually replace 3 rows where START_TIME > END_TIME in the activity files
        # 72 "2011-12-01 19:28:51  2011-12-01 16:29:59  Toileting"
        # to "2011-12-01 19:28:51  2011-19-01 16:29:59  Toileting"
        # 81 "2011-12-02 12:20:41  2011-12-01 10:20:59  Grooming"
        # to "2011-12-02 12:20:41  2011-12-01 12:20:59  Grooming"
        # 83 "2011-12-02 12:27:47  2011-12-01 11:35:49  Breakfast"
        # to "2011-12-02 12:27:47  2011-12-01 12:35:49  Breakfast"
        df_act.iat[69, 1] = pd.Timestamp('2011-12-01 19:29:59')
        df_act.iat[78, 1] = pd.Timestamp('2011-12-02 12:20:59')
        df_act.iat[80, 1] = pd.Timestamp('2011-12-02 12:35:49')

        df_act, correction_act = correct_activities(df_act, retain_corrections=retain_corrections)

    data.set_activity_df(df_act, subject)

    if retain_corrections:
        data.set_activity_correction(correction_act, subject)

    return data


def fix_OrdonezB_ADLS(path_to_file):
    """ fixes inconsistent use of tabs for delimiter in the file
    Parameters
    ----------
    path_to_file : str
        path to the file OrdonezB_ADLs.csv
    """
    
    path_corrected = path_to_file[:-17] + 'OrdonezB_ADLs_corr.txt'
    
    with open(path_to_file, 'r') as f_o, open(path_corrected, 'w') as f_t:
        for i, line in enumerate(f_o.readlines()):            
            if i in [0,1]: 
                f_t.write(line)  
                continue
            s = line.split()
            assert len(s) == 5
            new_line = s[0]+' '+s[1]+'\t\t'+s[2]+' '+s[3]+'\t\t'+s[4]                        
            f_t.write(new_line + "\n")
        f_t.close()
        f_o.close()

def _load_activities(act_path):
    df_act = pd.read_csv(act_path, delimiter='\t+', skiprows=[0,1], 
                         names=[START_TIME, END_TIME, ACTIVITY], engine='python')
    df_act[START_TIME] = pd.to_datetime(df_act[START_TIME])
    df_act[END_TIME] = pd.to_datetime(df_act[END_TIME])
    return df_act

def _load_devices(dev_path):
    df_dev = pd.read_csv(dev_path, delimiter='\t+', skiprows=[0, 1], 
                         names=[START_TIME, END_TIME, 'Location', 'Type', 'Place'], 
                         engine='python')
    df_dev[DEVICE] = df_dev['Place'] + ' ' + df_dev['Location'] + ' ' + df_dev['Type']
    
    # get room mapping devices
    df_locs = df_dev.copy().groupby([DEVICE, 'Type', 'Place', 'Location']).sum()
    df_locs = df_locs.reset_index().drop([START_TIME, END_TIME], axis=1)

    df_dev = df_dev[[START_TIME, END_TIME, DEVICE]]
    df_dev[START_TIME] = pd.to_datetime(df_dev[START_TIME])
    df_dev[END_TIME] = pd.to_datetime(df_dev[END_TIME])
    return df_dev, df_locs