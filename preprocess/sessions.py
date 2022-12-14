
import collections
import os
import pandas as pd
import numpy as np
from typing import Optional
from pathlib import Path


__author__ = 'Nuria'


_BMI_STIM_AGO = {
    'D13': [
        'ago13/221113/D02',
        'ago13/221114/D03',
        'ago13/221115/D04-2',
        'ago13/221116/D05',
    ],
    'D15': [
        'ago15/221113/D02',
        'ago15/221114/D03',
        'ago15/221115/D04-2',
        'ago15/221116/D05',
        'ago15/221117/D06-2',
        'ago15/221119/D08',
        'ago15/221119/D08-2',
    ],
    'D16': [
        'ago16/221113/D02',
        'ago16/221114/D03',
        'ago16/221116/D05',
        'ago16/221118/D07',
        'ago16/221118/D07-2',
        'ago16/221119/D08',
        'ago16/221119/D08-2',
    ],
    'D18': [
        'ago18/221113/D02',
        'ago18/221114/D03',
        'ago18/221116/D05',
        'ago18/221117/D06-2',
        'ago18/221118/D07',
        'ago18/221118/D07-2',
        'ago18/221118/D07-3',
    ],
}

_BMI_RANDOM = {
    'D13': [
        'ago13/221115/D04'],
    'D15': [
        'ago15/221115/D04',
        'ago15/221116/D05-2',
        'ago15/221117/D06',
        'ago15/221118/D07',
        'ago15/221118/D07-3',
    ],
    'D16': [
        'ago16/221115/D04',
        'ago16/221116/D05-2',
        'ago16/221117/D06',
        'ago16/221117/D06-2',
        'ago16/221119/D08-3',
    ],
    'D18': [
        'ago18/221115/D04',
        'ago18/221116/D05-2',
        'ago18/221117/D06',
        'ago18/221119/D08',
        'ago18/221119/D08-2',
    ],
}

_BMI_STIM = {
    'D13': [
        'ago13/221112/D01'],
    'D15': [
        'ago15/221112/D01'],
    'D16': [
        'ago16/221112/D01'],
    'D18': [
        'ago18/221112/D01'],
}

_BMI_AGO = {
    'D13': [
        'ago13/221117/D06'],
    'D15': [
        'ago15/221118/D07-2'],
    'D16': [
        'ago16/221115/D04-2'],
    'D18': [
        'ago18/221116/D05-3'],
}

_BEHAVIOR = {
    'D13': [
        'ago13/221113/D02'],
    'D15': [
        'ago15/221113/D02'],
    'D16': [
        'ago16/221113/D02'],
    'D18': [
        'ago18/221113/D02'],
}

_MOTOR_beh_before_BMI = {
    'D13': [
        'ago13/221113/D02',
        'ago13/221114/D03',
    ],
    'D15': [
        'ago15/221113/D02',
        'ago15/221114/D03',
    ],
    'D16': [
        'ago16/221113/D02',
        'ago16/221114/D03',
    ],
    'D18': [
        'ago18/221113/D02',
        'ago18/221114/D03',
    ]
}

_MOTOR_initial_behavior = {
    'D13': [
        'ago13/221113/D02',
    ],
    'D15': [
        'ago15/221113/D02',
    ],
    'D16': [
        'ago16/221113/D02',
    ],
    'D18': [
        'ago18/221113/D02',
    ]
}


def get_all_sessions() -> pd.DataFrame:
    """ function to get a df with all sessions"""
    df_BMI_STIM_AGO = pd.DataFrame(index=np.concatenate(list(_BMI_STIM_AGO.values())))
    df_BMI_STIM_AGO['experiment_type'] = 'BMI_STIM_AGO'
    df_BMI_RANDOM = pd.DataFrame(index=np.concatenate(list(_BMI_RANDOM.values())))
    df_BMI_RANDOM['experiment_type'] = 'BMI_CONTROL_RANDOM'
    df_BMI_STIM = pd.DataFrame(index=np.concatenate(list(_BMI_STIM.values())))
    df_BMI_STIM['experiment_type'] = 'BMI_CONTROL_LIGHT'
    df_BMI_AGO = pd.DataFrame(index=np.concatenate(list(_BMI_AGO.values())))
    df_BMI_AGO['experiment_type'] = 'BMI_CONTROL_AGO'
    df_experiments = pd.concat([pd.concat([df_BMI_STIM_AGO, df_BMI_RANDOM]),
                                pd.concat([df_BMI_STIM, df_BMI_AGO])])
    return df_experiments.sort_index().reset_index()


def get_sessions_df(folder_experiments: Path, experiment_type: str) -> pd.DataFrame:
    """ Function to retrieve the name of the sessions that will be used depending on the experiment type
    and the files that are useful for that experiment, baselines, bmis, behaviors, etc"""
    df_experiments = get_all_sessions()
    if experiment_type == 'BMI_STIM_AGO':
        dict_items = _BMI_STIM_AGO.items()
    elif experiment_type == 'BMI_CONTROL_RANDOM':
        dict_items = _BMI_RANDOM.items()
    elif experiment_type == 'BMI_CONTROL_LIGHT':
        dict_items = _BMI_STIM.items()
    elif experiment_type == 'BMI_CONTROL_AGO':
        dict_items = _BMI_AGO.items()
    elif experiment_type == 'BEHAVIOR':
        dict_items = _BEHAVIOR.items()
    else:
        raise ValueError(
            f'Could not find any controls for {experiment_type} '
            f'try BMI_STIM_AGO, BMI_CONTROL_RANDOM, BMI_CONTROL_LIGHT, BMI_CONTROL_AGO or BEHAVIOR')
    ret = collections.defaultdict(list)
    for mice_name, sessions_per_type in dict_items:
        for day_index, session_path in enumerate(sessions_per_type):
            [mice_name, session_date, day_init] = session_path.split('/')
            ret['mice_name'].append(mice_name)
            ret['session_date'].append(session_date)
            ret['day_init'].append(day_init)
            location_session = np.where(df_experiments["index"] == session_path)[0][0]
            if day_init[-2:] == '-2':
                ret['session_day'].append('2nd')
                ret['previous_session'].append(df_experiments.iloc[location_session - 1].experiment_type)
            elif day_init[-2:] == '-3':
                ret['session_day'].append('3rd')
                ret['previous_session'].append(df_experiments.iloc[location_session - 1].experiment_type)
            else:
                ret['session_day'].append('1st')
                ret['previous_session'].append('None')
            ret['experiment_type'].append(experiment_type)
            ret['session_path'].append(session_path)
            ret['day_index'].append(day_index)

            dir_files = Path(folder_experiments) / session_path
            for file_name in os.listdir(dir_files):
                if experiment_type != 'BEHAVIOR':
                    if file_name[:2] == 'im':
                        dir_im = Path(folder_experiments) / session_path / 'im'
                        for file_name_im_dir in os.listdir(dir_im):
                            dir_im2 = dir_im / file_name_im_dir
                            for file_name_im_file in os.listdir(dir_im2):
                                if file_name_im_file[:8] == 'baseline':
                                    ret['Baseline_im'].append(file_name_im_file)
                                    ret['Voltage_Baseline'].append(file_name_im_file + '_Cycle00001_VoltageRecording_001.csv')
                                elif file_name_im_file[:8] in ['BMI_stim', 'RandomDR']:
                                    ret['Voltage_rec'].append(file_name_im_file + '_Cycle00001_VoltageRecording_001.csv')
                                    ret['Experiment_im'].append(file_name_im_file)
                                    ret['Experiment_dir'].append(file_name_im_dir)

                    if file_name[:10] == 'BaselineOn':
                        ret['Baseline_online'].append(file_name)
                    elif file_name[:10] == 'BMI_online':
                        ret['BMI_online'].append(file_name)
                    elif file_name[:10] == 'BMI_target':
                        ret['BMI_target'].append(file_name)
                    elif file_name[:8] == 'roi_data':
                        ret['roi_data'].append(file_name)
                    elif file_name[:8] == 'strcMask':
                        ret['mask_data'].append(file_name)
                    elif file_name[:10] == 'target_cal':
                        ret['target_calibration'].append(file_name)

                if file_name[:2] == 'mo':
                    dir_motor = Path(folder_experiments) / session_path / 'motor'
                    for file_name_motor_file in os.listdir(dir_motor):
                        if file_name_motor_file[-7:-4] in ['ine', 'BMI']:
                            [_, trigger_XY, _, baseline_BMI] = file_name_motor_file.split('_')
                            if trigger_XY == 'XY':
                                if baseline_BMI == 'baseline.csv':
                                    ret['XY_baseline'].append(file_name_motor_file)
                                elif baseline_BMI == 'BMI.csv':
                                    ret['XY_BMI'].append(file_name_motor_file)
                            elif trigger_XY == 'Trigger':
                                if baseline_BMI == 'baseline.csv':
                                    ret['trigger_baseline'].append(file_name_motor_file)
                                elif baseline_BMI == 'BMI.csv':
                                    ret['trigger_BMI'].append(file_name_motor_file)
            if session_path == 'ago18/221117/D06':
                ret['roi_data'].append('missing')
                ret['mask_data'].append('missing')

    return pd.DataFrame(ret)


def get_behav_df(folder_experiments: Path, experiment_type: str) -> pd.DataFrame:
    """ Function to retrieve the name of the sessions that will be used depending on the experiment type
    and the files that are useful for that experiment, baselines, bmis, behaviors, etc"""
    if experiment_type == 'Initial_behavior':
        dict_items = _MOTOR_initial_behavior.items()
        ending_str = 'ior'
    elif experiment_type == 'Behavior_before':
        dict_items = _MOTOR_beh_before_BMI.items()
        ending_str = 'ore'
    else:
        raise ValueError(
            f'Could not find any controls for {experiment_type} try Initial_behavior, Behavior_before')
    ret = collections.defaultdict(list)
    for mice_name, sessions_per_type in dict_items:
        for day_index, session_path in enumerate(sessions_per_type):
            [mice_name, session_date, day_init] = session_path.split('/')
            ret['mice_name'].append(mice_name)
            ret['session_date'].append(session_date)
            ret['day_init'].append(day_init)
            ret['experiment_type'].append(experiment_type)
            ret['session_path'].append(session_path)
            ret['day_index'].append(day_index)

            dir_files = Path(folder_experiments) / session_path
            for file_name in os.listdir(dir_files):
                if file_name[:2] == 'mo':
                    dir_motor = Path(folder_experiments) / session_path / 'motor'
                    for file_name_motor_file in os.listdir(dir_motor):
                        # TODO check ending for behav and inital
                        if file_name_motor_file[-7:-4] == ending_str:
                            [_, trigger_XY, _, _, _] = file_name_motor_file.split('_')
                            if trigger_XY == 'XY':
                                ret['XY'].append(file_name_motor_file)
                            elif trigger_XY == 'Trigger':
                                ret['trigger'].append(file_name_motor_file)

    return pd.DataFrame(ret)

