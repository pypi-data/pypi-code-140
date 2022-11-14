import numpy as np
from scipy.integrate import cumtrapz
from worklab.utils import lowpass_butter
from worklab.imu import push_imu
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def peaks_plot(sessiondata, name=''):
    """
    Plot peaks  plot

    Parameters
    ----------
    sessiondata : str
        processed sessiondata structure
    name : str
        name of a session

    Returns
    -------
    ax: axis object

    """
    vel = "vel"

    move = sessiondata['frame'][(sessiondata['frame'][vel] < -0.1) | (sessiondata['frame'][vel] > 0.1)].reset_index(
        drop=True)
    rotate = move[abs(move['rot_vel']) > 10].reset_index(drop=True)
    forward = sessiondata['frame'][(sessiondata['frame'][vel]) > 0.1].reset_index(drop=True)

    fig, [ax1, ax2] = plt.subplots(2, 1, figsize=[14, 10])
    ax1.plot(forward['time'], forward[vel])
    peaks, properties = find_peaks(forward[vel], prominence=0.5, distance=50, width=50, height=2)
    ax1.plot(forward['time'][peaks], forward[vel][peaks], 'k.')
    ax1.set_ylabel("Velocity [m/s]", fontsize=10)
    ax1.tick_params(axis='y', labelsize=10)
    ax1.tick_params(axis='x', labelsize=10)
    ax1.set_title(f"{name} Velocity with peaks")

    ax2.plot(rotate['time'], rotate['rot_vel'])
    peaks2, _ = find_peaks(rotate['rot_vel'], prominence=50, height=90, width=20, distance=50)
    peaks3, _ = find_peaks(-rotate['rot_vel'], prominence=50, height=90, width=20, distance=50)
    ax2.plot(rotate['time'][peaks2], rotate['rot_vel'][peaks2], 'k.')
    ax2.plot(rotate['time'][peaks3], rotate['rot_vel'][peaks3], 'k.')
    ax2.set_xlabel("Time [s]", fontsize=10)
    ax2.set_ylabel("Rotational velocity [deg/s]", fontsize=10)
    ax2.tick_params(axis='y', labelsize=10)
    ax2.tick_params(axis='x', labelsize=10)
    ax2.set_title(f"{name} Rotational velocity with peaks")

    return fig, ax1, ax2


def peaks_rot_vel_plot(sessiondata, side: bool = True):
    """
    Plot peaks  plot

    Parameters
    ----------
    sessiondata : str
        processed sessiondata structure
    side : bool
        if set to True left side is analysed
        if set to False right side is analysed

    Returns
    -------
    ax: axis object

    """
    vel = "vel"
    # Cut the dataset in part where there was movement
    move = sessiondata['frame'][(sessiondata['frame'][vel] < -0.1) | (sessiondata['frame'][vel] > 0.1)].reset_index(
        drop=True)

    if side is True:  # left
        rotate = move[move['rot_vel'] > 10].reset_index(drop=True)
    else:  # right
        rotate = move[move['rot_vel'] < -10].reset_index(drop=True)
        rotate['rot_vel'] = -rotate['rot_vel']

    turn1 = rotate[(rotate[vel] > -0.5) & (rotate[vel] < 0.5)].reset_index(drop=True)
    turn2 = rotate[(rotate[vel] > -1.5) & (rotate[vel] < 1.5)].reset_index(drop=True)
    curve1 = rotate[(rotate[vel] > 1) & (rotate[vel] < 2)].reset_index(drop=True)
    curve2 = rotate[rotate[vel] > 1.5].reset_index(drop=True)

    moves = [turn1, turn2, curve1, curve2]
    moves_keys = ['turn1', 'turn2', 'curve1', 'curve2']
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=[14, 10])
    axes = [ax1, ax2, ax3, ax4]
    for movement, keys, axi in zip(moves, moves_keys, axes):
        peaks, _ = find_peaks(movement['rot_vel'], prominence=50, height=90, width=20, distance=50)
        axi.plot(movement['time'], movement['rot_vel'])
        axi.plot(movement['time'][peaks], movement['rot_vel'][peaks], 'k.')
        axi.set_ylabel("Rotational velocity [deg/s]", fontsize=10)
        axi.set_title(keys)

    return fig, ax1, ax2, ax3, ax4


def straight_sprint_plot(data, name=''):
    """
    Plot straight sprint plot

    Parameters
    ----------
    data : pd.Series
        processed sprint pd.Series
    name : str
        name of a session

    Returns
    -------
    ax: axis object

    """
    vel = "vel"

    vel = data[vel]
    time = data['time']
    dist = data['dist']
    rot_vel = data['rot_vel']

    sfreq = 1 / time.diff().mean()

    # Determine distance in x and y direction
    dist_y = cumtrapz(
        np.gradient(dist) * np.sin(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)
    dist_x = cumtrapz(
        np.gradient(dist) * np.cos(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)

    # Calculate vel_peak and position of vel_peak
    y_max_vel = vel.idxmax()
    y_max_vel_value = np.max(vel)

    # Define vel zones
    vel_sin_2 = dist_y[vel > 2]
    vel_cos_2 = dist_x[vel > 2]
    vel_sin_3 = dist_y[vel > 3]
    vel_cos_3 = dist_x[vel > 3]
    vel_sin_4 = dist_y[vel > 4]
    vel_cos_4 = dist_x[vel > 4]

    # Create straight sprint figure
    plt.style.use("seaborn-darkgrid")
    fig, ax = plt.subplots(1, 1, figsize=[10, 6])
    ax.set_xlim(-6, 6)
    ax.set_ylim(0, max(dist_x) + 1)
    ax.plot(-dist_y, dist_x)
    ax.plot(-vel_sin_2, vel_cos_2, 'y.', markersize=5,
            label='vel > 2 m/s')
    ax.plot(-vel_sin_3, vel_cos_3, 'g.', markersize=8,
            label='vel > 3 m/s')
    ax.plot(-vel_sin_4, vel_cos_4, 'r.', markersize=14,
            label='vel > 4 m/s')
    ax.plot(-dist_y[y_max_vel],
            dist_x[y_max_vel], 'ko', markersize=10,
            label='$vel_{peak}$: ' + str(round(y_max_vel_value, 2)) + ' m/s')
    ax.set_xlabel("Distance [m]", fontsize=12)
    ax.set_ylabel("Distance [m]", fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.set_title(f"{name} Sprint test")
    ax.legend()

    return ax


def overview_sprint_plot(data, name=''):
    """
    Plot overview straight sprint test

    Parameters
    ----------
    data : pd.Series
        processed sprint pd.Series
    name : str
        name of a session

    Returns
    -------
    ax: axis object

    """
    vel = "vel"

    vel = data[vel]
    time = data['time']
    dist = data['dist']
    rot_vel = data['rot_vel']

    sfreq = 1 / time.diff().mean()

    # Calculate processed acceleration from velocity
    acc = lowpass_butter(np.gradient(vel) * sfreq, sfreq=sfreq, cutoff=10)

    # Calculate push detection with function
    push_idx, acc_filt, n_pushes, cycle_time, push_freq = push_imu(acc, sfreq)

    # Calculate distance in x and y direction
    dist_y = cumtrapz(
        np.gradient(dist) * np.sin(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)
    dist_x = cumtrapz(
        np.gradient(dist) * np.cos(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)

    # Calculate vel zones, vel_peak and acc_peak
    y_max_vel = vel.idxmax()
    y_max_acc = acc.argmax()
    y_max_vel_value = np.max(vel)
    y_max_acc_value = np.max(acc)
    vel_sin_2 = dist_y[vel > 2]
    vel_cos_2 = dist_x[vel > 2]
    vel_sin_3 = dist_y[vel > 3]
    vel_cos_3 = dist_x[vel > 3]
    vel_sin_4 = dist_y[vel > 4]
    vel_cos_4 = dist_x[vel > 4]

    # Create time vs. velocity with push detection figure
    plt.style.use("seaborn-darkgrid")
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=[14, 10])
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    fig.suptitle(f"{name} Overview Sprint test")
    ax1.set_ylim(-6, 6)
    ax1.plot(time, vel, 'r')
    ax1.plot(time[push_idx], vel[push_idx], 'k.')
    ax1.set_xlabel("Time [s]", fontsize=10)
    ax1.set_ylabel("Velocity [m/s]", fontsize=10)
    ax1.tick_params(axis='y', colors='r', labelsize=10)
    ax1.tick_params(axis='x', labelsize=10)
    ax1.yaxis.label.set_color('r')
    ax1.autoscale(axis='x', tight=True)

    # Create time vs. acceleration with push detection figure
    ax5 = ax1.twinx()
    ax5.set_ylim(-30, 30)
    ax5.plot(time, acc, 'C7', alpha=0.5)
    ax5.plot(time, acc_filt, 'b')
    ax5.plot(time[push_idx], acc_filt[push_idx], 'k.')
    ax5.set_ylabel("Acceleration [m/$s^2$]", fontsize=10)
    ax5.tick_params(axis='y', colors='b', labelsize=10)
    ax5.yaxis.label.set_color('b')
    ax5.autoscale(axis='x', tight=True)

    # Create time vs. velocity figure with vel_peak
    ax2.set_ylim(0, y_max_vel_value + 0.5)
    ax2.plot(time, vel, 'r')
    ax2.plot(time[y_max_vel], vel[y_max_vel], 'k.',
             label='Vel$_{peak}$: ' + str(round(y_max_vel_value, 2)) + ' m/s')
    ax2.set_xlabel("Time [s]", fontsize=10)
    ax2.set_ylabel("Velocity [m/s]", fontsize=10)
    ax2.tick_params(axis='y', colors='r', labelsize=10)
    ax2.tick_params(axis='x', labelsize=10)
    ax2.yaxis.label.set_color('r')
    ax2.legend(loc='lower right', prop={'size': 10})
    ax2.autoscale(axis='x', tight=True)

    # Create time vs. distance figure
    ax6 = ax2.twinx()
    ax6.set_ylim(0, max(dist) + 1)
    ax6.plot(time, dist)
    ax6.plot(time[y_max_vel], dist[y_max_vel], 'k.')
    ax6.set_ylabel("Distance [m]", fontsize=10)
    ax6.tick_params(axis='y', colors='b', labelsize=10)
    ax6.yaxis.label.set_color('b')
    ax2.autoscale(axis='x', tight=True)

    # Create time vs. acceleration figure with acc_peak
    ax3.set_ylim(np.min(acc) - 1, y_max_acc_value + 1)
    ax3.plot(time, acc, 'g')
    ax3.plot(time[y_max_acc], acc[y_max_acc], 'k.',
             label='Acc$_{peak}$: ' + str(round(y_max_acc_value, 2)) + ' m/$s^2$')
    ax3.set_xlabel("Time [s]", fontsize=10)
    ax3.set_ylabel("Acceleration [m/$s^2$]", fontsize=10)
    ax3.tick_params(axis='y', colors='g', labelsize=10)
    ax3.tick_params(axis='x', labelsize=10)
    ax3.yaxis.label.set_color('g')
    ax3.legend(loc='lower center', prop={'size': 10})
    ax3.autoscale(axis='x', tight=True)

    # Create time vs. distance figure
    ax7 = ax3.twinx()
    ax7.set_ylim(0, max(dist) + 1)
    ax7.plot(time, dist)
    ax7.plot(time[y_max_acc], dist[y_max_acc], 'k.')
    ax7.set_ylabel("Distance [m]", fontsize=10)
    ax7.tick_params(axis='y', colors='b', labelsize=10)
    ax7.yaxis.label.set_color('b')
    ax3.autoscale(axis='x', tight=True)

    # Create Straight sprint figure with vel zones and vel_peak
    ax4.set_xlim(-10, 10)
    ax4.set_ylim(0, max(dist_x) + 1)
    # ax4.text(3, max(dist)-2, 'Endtime: ' + str(round(len(time) / sfreq, 2)) +'s',
    #          bbox=dict(facecolor='green', alpha=0.5))
    ax4.plot(-dist_y, dist_x)
    ax4.plot(-vel_sin_2, vel_cos_2, 'y.', markersize=5,
             label='Vel > 2 m/s')
    ax4.plot(-vel_sin_3, vel_cos_3, 'g.', markersize=8,
             label='Vel > 3 m/s')
    ax4.plot(-vel_sin_4, vel_cos_4, 'r.', markersize=14,
             label='Vel > 4 m/s')
    ax4.plot(-dist_y[y_max_vel],
             dist_x[y_max_vel], 'ko', markersize=10,
             label='Vel$_{peak}$: ' + str(round(y_max_vel_value, 2)) + ' m/s')
    ax4.set_xlabel("Distance [m]", fontsize=10)
    ax4.set_ylabel("Distance [m]", fontsize=10)
    ax4.tick_params(axis='y', labelsize=10)
    ax4.tick_params(axis='x', labelsize=10)
    ax4.legend(loc='upper left', prop={'size': 8})

    return ax1, ax2, ax3, ax4, ax5, ax6, ax7


def butterfly_plot(data, name='', mirror=False):
    """
    Plot butterfly sprint test

    Parameters
    ----------
    data : pd.Series
        processed butterfly pd.Series
    name : str
        name of a session
    mirror : bool
        make true if test is executed in reversed order

    Returns
    -------
    ax: axis object

    """
    time = data['time']
    dist = data['dist']
    rot_vel = data['rot_vel']

    sfreq = 1 / time.diff().mean()
    # Determine distance in x and y direction
    dist_y = cumtrapz(
        np.gradient(dist) * np.sin(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)
    dist_x = cumtrapz(
        np.gradient(dist) * np.cos(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)

    # Change signal if test was executed in reversed order
    if mirror is True:
        dist_y = -dist_y
        dist_x = -dist_x

    # Caculate rotational vel zones and rot_vel_peak, rot_acc_peak
    rot_vel.reset_index(inplace=True, drop=True)
    rot_vel_y_45 = dist_y[rot_vel.abs() > 45]
    rot_vel_x_45 = dist_x[rot_vel.abs() > 45]
    rot_vel_y_90 = dist_y[rot_vel.abs() > 90]
    rot_vel_x_90 = dist_x[rot_vel.abs() > 90]
    rot_vel_y_180 = dist_y[rot_vel.abs() > 180]
    rot_vel_x_180 = dist_x[rot_vel.abs() > 180]
    rot_acc = np.gradient(rot_vel) * sfreq
    y_max_rot_vel = rot_vel.idxmax()
    y_max_rot_acc = np.argmax(rot_acc)
    y_max_rot_vel_value = np.max(rot_vel)
    y_max_rot_acc_value = np.max(rot_acc)

    # Create butterfly sprint figure
    plt.style.use("seaborn-darkgrid")
    fig, ax = plt.subplots(1, 1, figsize=[10, 6])
    ax.text(2, 7, 'Endtime: ' + str(round(len(time) / sfreq, 2)) + 's',
            bbox=dict(facecolor='green', alpha=0.5))
    ax.plot(dist_x, dist_y)
    ax.plot(rot_vel_x_45, rot_vel_y_45, 'y.', markersize=5,
            label='Rot vel > 45 deg/s')
    ax.plot(rot_vel_x_90, rot_vel_y_90, 'g.', markersize=8,
            label='Rot vel > 90 deg/s')
    ax.plot(rot_vel_x_180, rot_vel_y_180, 'r.', markersize=14,
            label='Rot vel > 180 deg/s')
    ax.plot(dist_x[y_max_rot_vel],
            dist_y[y_max_rot_vel], 'ko', markersize=10,
            label='Rot vel$_{peak}$: ' + str(int(y_max_rot_vel_value)) + ' deg/s')
    ax.plot(dist_x[y_max_rot_acc],
            dist_y[y_max_rot_acc], 'k*', markersize=10,
            label='Rot acc$_{peak}:$ ' + str(int(y_max_rot_acc_value)) + ' deg/$s^2$')
    ax.set_xlabel("Distance [m]", fontsize=12)
    ax.set_ylabel("Distance [m]", fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.set_title(f"{name} Butterfly test")
    ax.legend(loc='upper left', prop={'size': 10})

    return ax


def overview_butterfly_plot(data, name='', mirror=False):
    """
    Plot butterfly sprint test overview

    Parameters
    ----------
    data : pd.Series
        processed butterfly pd.Series
    name : str
        name of a session
    mirror : bool
        make true if test is executed in reversed order
    Returns
    -------
    ax: axis object

    """
    vel = "vel"

    vel = data[vel]
    time = data['time']
    dist = data['dist']
    rot_vel = data['rot_vel']

    sfreq = 1 / time.diff().mean()

    # Calculate processed acceleration from velocity
    acc = lowpass_butter(np.gradient(vel) * sfreq, sfreq=sfreq, cutoff=10)

    # Calculate distance in x and y direction
    dist_y = cumtrapz(
        np.gradient(dist) * np.sin(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)
    dist_x = cumtrapz(
        np.gradient(dist) * np.cos(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)

    # Change signal if test was executed in reversed order
    if mirror is True:
        dist_y = -dist_y
        dist_x = -dist_x

    # Caculate rotational vel zones and rot_vel_peak, rot_acc_peak
    rot_vel.reset_index(inplace=True, drop=True)
    rot_vel_y_45 = dist_y[rot_vel.abs() > 45]
    rot_vel_x_45 = dist_x[rot_vel.abs() > 45]
    rot_vel_y_90 = dist_y[rot_vel.abs() > 90]
    rot_vel_x_90 = dist_x[rot_vel.abs() > 90]
    rot_vel_y_180 = dist_y[rot_vel.abs() > 180]
    rot_vel_x_180 = dist_x[rot_vel.abs() > 180]
    rot_acc = np.gradient(rot_vel) * sfreq
    y_max_rot_vel = rot_vel.idxmax()
    y_max_rot_acc = np.argmax(rot_acc)
    y_max_rot_vel_value = np.max(rot_vel)
    y_max_rot_acc_value = np.max(rot_acc)
    y_max_vel = vel.idxmax()
    y_max_acc = acc.argmax()
    y_max_vel_value = np.max(vel)
    y_max_acc_value = np.max(acc)

    # Create time vs. rotational velocity figure
    plt.style.use("seaborn-darkgrid")
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=[14, 10])
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    fig.suptitle(f"{name} Overview Butterfly test")
    ax1.set_ylim(np.min(rot_vel) - 10, np.max(rot_vel) + 10)
    ax1.plot(time, rot_vel, 'b')
    ax1.set_xlabel("Time [s]", fontsize=10)
    ax1.set_ylabel("Rotational velocity [deg/s]", fontsize=10)
    ax1.tick_params(axis='y', colors='b', labelsize=10)
    ax1.tick_params(axis='x', labelsize=10)
    ax1.yaxis.label.set_color('b')
    ax1.autoscale(axis='x', tight=True)

    # Create time vs. velocity figure with vel_peak
    ax2.set_ylim(0, y_max_vel_value + 0.5)
    ax2.plot(time, vel, 'r')
    ax2.plot(time[y_max_vel], vel[y_max_vel], 'k.',
             label='Vel$_{peak}$: ' + str(round(y_max_vel_value, 2)) + ' m/s')
    ax2.set_xlabel("Time [s]", fontsize=10)
    ax2.set_ylabel("Velocity [m/s]", fontsize=10)
    ax2.tick_params(axis='y', colors='r', labelsize=10)
    ax2.tick_params(axis='x', labelsize=10)
    ax2.yaxis.label.set_color('r')
    ax2.legend()
    ax2.autoscale(axis='x', tight=True)

    # Create time vs. acceleration figure with acc_peak
    ax3.set_ylim(np.min(acc) - 1, y_max_acc_value + 1)
    ax3.plot(time, acc, 'g')
    ax3.plot(time[y_max_acc], acc[y_max_acc], 'k.',
             label='Acc$_{peak}$: ' + str(round(y_max_acc_value, 2)) + ' m/$s^2$')
    ax3.set_xlabel("Time [s]", fontsize=10)
    ax3.set_ylabel("Acceleration [m/$s^2$]", fontsize=10)
    ax3.tick_params(axis='y', colors='g', labelsize=10)
    ax3.tick_params(axis='x', labelsize=10)
    ax3.yaxis.label.set_color('g')
    ax3.legend()

    # Create butterfly sprint figure
    ax4.plot(dist_x, dist_y)
    ax4.text(2, 7, 'Endtime: ' + str(round(len(time) / sfreq, 2)) + 's',
             bbox=dict(facecolor='green', alpha=0.5))
    ax4.plot(rot_vel_x_45, rot_vel_y_45, 'y.', markersize=6,
             label='Rot vel > 45 deg/s')
    ax4.plot(rot_vel_x_90, rot_vel_y_90, 'g.', markersize=8,
             label='Rot vel > 90 deg/s')
    ax4.plot(rot_vel_x_180, rot_vel_y_180, 'r.', markersize=14,
             label='Rot vel > 180 deg/s')
    ax4.plot(dist_x[y_max_rot_vel],
             dist_y[y_max_rot_vel], 'ko', markersize=10,
             label='Rot vel$_{peak}$: ' + str(int(y_max_rot_vel_value)) + ' deg/s')
    ax4.plot(dist_x[y_max_rot_acc],
             dist_y[y_max_rot_acc], 'k*', markersize=10,
             label='Rot acc$_{peak}$: ' + str(int(y_max_rot_acc_value)) + ' deg/$s^2$')
    ax4.set_xlabel("Distance [m]", fontsize=10)
    ax4.set_ylabel("Distance [m]", fontsize=10)
    ax4.tick_params(axis='y', labelsize=10)
    ax4.tick_params(axis='x', labelsize=10)
    ax4.legend(loc='upper left', prop={'size': 8})

    return ax1, ax2, ax3, ax4


def spider_plot(data, name='', mirror=False):
    """
    Plot spider test

    Parameters
    ----------
    data : pd.Series
        processed spider pd.Series
    name : str
        name of a session
    mirror : bool
        make true if test is executed in reversed order

    Returns
    -------
    ax: axis object

    """
    time = data['time']
    dist = data['dist']
    rot_vel = data['rot_vel']

    sfreq = 1 / time.diff().mean()

    # Calculate distance in x and y direction
    dist_y = cumtrapz(
        np.gradient(dist) * np.sin(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)
    dist_x = cumtrapz(
        np.gradient(dist) * np.cos(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)

    # Change signal if test was executed in reversed order
    if mirror is True:
        dist_x = -dist_x
        dist_y = -dist_y

    # Caculate rotational vel zones and rot_vel_peak, rot_acc_peak
    rot_vel.reset_index(inplace=True, drop=True)
    rot_vel_y_45 = dist_y[rot_vel.abs() > 45]
    rot_vel_x_45 = dist_x[rot_vel.abs() > 45]
    rot_vel_y_90 = dist_y[rot_vel.abs() > 90]
    rot_vel_x_90 = dist_x[rot_vel.abs() > 90]
    rot_vel_y_180 = dist_y[rot_vel.abs() > 180]
    rot_vel_x_180 = dist_x[rot_vel.abs() > 180]
    rot_acc = np.gradient(rot_vel) * sfreq
    y_max_rot_vel = rot_vel.idxmax()
    y_max_rot_acc = np.argmax(rot_acc)
    y_max_rot_vel_value = np.max(rot_vel)
    y_max_rot_acc_value = np.max(rot_acc)

    # Create Spider figure
    plt.style.use("seaborn-darkgrid")
    fig, ax = plt.subplots(1, 1, figsize=[10, 6])
    if mirror is True:
        ax.text(0.8, 3.1, 'Endtime: ' + str(round(len(time) / sfreq, 2)) + 's',
                bbox=dict(facecolor='green', alpha=0.5))
    else:
        ax.text(2.7, 3.1, 'Endtime: ' + str(round(len(time) / sfreq, 2)) + 's',
                bbox=dict(facecolor='green', alpha=0.5))
    ax.plot(-dist_x, -dist_y)
    ax.plot(-rot_vel_x_45, -rot_vel_y_45, 'y.', markersize=5,
            label='Rot vel > 45 deg/s')
    ax.plot(-rot_vel_x_90, -rot_vel_y_90, 'g.', markersize=8,
            label='Rot vel > 90 deg/s')
    ax.plot(-rot_vel_x_180, -rot_vel_y_180, 'r.', markersize=14,
            label='Rot vel > 180 deg/s')
    ax.plot(-dist_x[y_max_rot_vel],
            -dist_y[y_max_rot_vel], 'ko', markersize=10,
            label='Rot vel$_{peak}:$ ' + str(int(y_max_rot_vel_value)) + ' deg/s')
    ax.plot(-dist_x[y_max_rot_acc],
            -dist_y[y_max_rot_acc], 'k*', markersize=10,
            label='Rot acc$_{peak}:$ ' + str(int(y_max_rot_acc_value)) + ' deg/s$^{2}$')
    ax.set_xlabel("Distance [m]", fontsize=12)
    ax.set_ylabel("Distance [m]", fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.set_title(f"{name} Spider test")
    ax.legend(loc='upper left', prop={'size': 10})

    return ax


def overview_spider_plot(data, name='', mirror=False):
    """
    Plot spider test

    Parameters
    ----------
    data : pd.Series
        processed spider pd.Series
    name : str
        name of a session
    mirror : bool
        make true if test is executed in reversed order
    Returns
    -------
    ax: axis object

    """
    vel = "vel"

    vel = data[vel]
    time = data['time']
    dist = data['dist']
    rot_vel = data['rot_vel']

    sfreq = 1 / time.diff().mean()

    # Calculate processed acceleration from velocity
    acc = lowpass_butter(np.gradient(vel) * sfreq, sfreq=sfreq, cutoff=10)

    # Calculate distance in x and y direction
    dist_y = cumtrapz(
        np.gradient(dist) * np.sin(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)
    dist_x = cumtrapz(
        np.gradient(dist) * np.cos(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)

    # Change signal if test was executed in reversed order
    if mirror is True:
        dist_x = -dist_x
        dist_y = -dist_y

    # Calculate rotational vel zones and rot_vel_peak, rot_acc_peak
    rot_vel.reset_index(inplace=True, drop=True)
    rot_vel_y_45 = dist_y[rot_vel.abs() > 45]
    rot_vel_x_45 = dist_x[rot_vel.abs() > 45]
    rot_vel_y_90 = dist_y[rot_vel.abs() > 90]
    rot_vel_x_90 = dist_x[rot_vel.abs() > 90]
    rot_vel_y_180 = dist_y[rot_vel.abs() > 180]
    rot_vel_x_180 = dist_x[rot_vel.abs() > 180]
    rot_acc = np.gradient(rot_vel) * sfreq
    y_max_rot_vel = rot_vel.idxmax()
    y_max_rot_acc = np.argmax(rot_acc)
    y_max_rot_vel_value = np.max(rot_vel)
    y_max_rot_acc_value = np.max(rot_acc)
    y_max_vel = vel.idxmax()
    y_max_acc = acc.argmax()
    y_max_vel_value = np.max(vel)
    y_max_acc_value = np.max(acc)

    # Create time vs. rotational velocity figure
    plt.style.use("seaborn-whitegrid")
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=[14, 10])
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    fig.suptitle(f"{name} Overview Spider test")
    ax1.set_ylim(np.min(rot_vel) - 10, np.max(rot_vel) + 10)
    ax1.plot(time, rot_vel, 'b')
    ax1.set_xlabel("Time [s]", fontsize=10)
    ax1.set_ylabel("Rotational velocity [deg/s]", fontsize=10)
    ax1.tick_params(axis='y', colors='b', labelsize=10)
    ax1.tick_params(axis='x', labelsize=10)
    ax1.yaxis.label.set_color('b')
    ax1.autoscale(axis='x', tight=True)

    # Create time vs. velocity figure with vel_peak
    ax2.set_ylim(0, y_max_vel_value + 0.5)
    ax2.plot(time, vel, 'r')
    ax2.plot(time[y_max_vel], vel[y_max_vel], 'k.',
             label='Vel$_{peak}$: ' + str(round(y_max_vel_value, 2)) + ' m/s')
    ax2.set_xlabel("Time [s]", fontsize=10)
    ax2.set_ylabel("Velocity [m/s]", fontsize=10)
    ax2.tick_params(axis='y', colors='r', labelsize=10)
    ax2.tick_params(axis='x', labelsize=10)
    ax2.yaxis.label.set_color('r')
    ax2.legend(loc='lower right', prop={'size': 8})
    ax2.autoscale(axis='x', tight=True)

    # Create time vs. acceleration figure with acc_peak
    ax3.set_ylim(np.min(acc) - 1, y_max_acc_value + 1)
    ax3.plot(time, acc, 'g')
    ax3.plot(time[y_max_acc], acc[y_max_acc], 'k.',
             label='Acc$_{peak}$: ' + str(round(y_max_acc_value, 2)) + ' m/$s^2$')
    ax3.set_xlabel("Time [s]", fontsize=10)
    ax3.set_ylabel("Acceleration [m/$s^2$]", fontsize=10)
    ax3.tick_params(axis='y', colors='g', labelsize=10)
    ax3.tick_params(axis='x', labelsize=10)
    ax3.yaxis.label.set_color('g')
    ax3.legend(loc='lower center', prop={'size': 10})
    ax3.autoscale(axis='x', tight=True)

    # Create Spider figure
    ax4.set_ylim(-0.5, 3)
    ax4.set_xlim(-3, 2)
    ax4.text(1, 3, 'Endtime: ' + str(round(len(time) / sfreq, 2)) + 's',
             bbox=dict(facecolor='green', alpha=0.5))
    ax4.plot(-dist_x, -dist_y)
    ax4.plot(-rot_vel_x_45, -rot_vel_y_45, 'y.', markersize=5,
             label='rot_vel > 45 deg/s')
    ax4.plot(-rot_vel_x_90, -rot_vel_y_90, 'g.', markersize=8,
             label='rot_vel > 90 deg/s')
    ax4.plot(-rot_vel_x_180, -rot_vel_y_180, 'r.', markersize=14,
             label='rot_vel > 180 deg/s')
    ax4.plot(-dist_x[y_max_rot_vel],
             -dist_y[y_max_rot_vel], 'ko', markersize=10,
             label='rot_$vel_{peak}$: ' + str(int(y_max_rot_vel_value)) + ' deg/s')
    ax4.plot(-dist_x[y_max_rot_acc],
             -dist_y[y_max_rot_acc], 'k*', markersize=10,
             label='rot_$acc_{peak}$: ' + str(int(y_max_rot_acc_value)) + ' deg/$s^2$')
    ax4.set_xlabel("Distance [m]", fontsize=10)
    ax4.set_ylabel("Distance [m]", fontsize=10)
    ax4.tick_params(axis='y', labelsize=10)
    ax4.tick_params(axis='x', labelsize=10)
    ax4.legend(loc='upper left', prop={'size': 8})

    return ax1, ax2, ax3, ax4


def illinois_plot(data, name='', mirror=False):
    """
    Plot illinois test

    Parameters
    ----------
    data : pd.Series
        processed illinois pd.Series
    name : str
        name of a session
    mirror : bool
        make true if test is executed in reversed order

    Returns
    -------
    ax: axis object

    """
    time = data['time']
    dist = data['dist']
    rot_vel = data['rot_vel']

    sfreq = 1 / time.diff().mean()

    # Calculate distance in x and y direction
    dist_y = cumtrapz(
        np.gradient(dist) * np.sin(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)
    dist_x = cumtrapz(
        np.gradient(dist) * np.cos(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)

    # Change signal if test was executed in reversed order
    if mirror is True:
        dist_x = -dist_x
        dist_y = -dist_y

    # Caculate rotational vel zones and rot_vel_peak, rot_acc_peak
    rot_vel.reset_index(inplace=True, drop=True)
    rot_vel_y_45 = dist_y[rot_vel.abs() > 45]
    rot_vel_x_45 = dist_x[rot_vel.abs() > 45]
    rot_vel_y_90 = dist_y[rot_vel.abs() > 90]
    rot_vel_x_90 = dist_x[rot_vel.abs() > 90]
    rot_vel_y_180 = dist_y[rot_vel.abs() > 180]
    rot_vel_x_180 = dist_x[rot_vel.abs() > 180]
    rot_acc = np.gradient(rot_vel) * sfreq
    y_max_rot_vel = rot_vel.idxmax()
    y_max_rot_acc = np.argmax(rot_acc)
    y_max_rot_vel_value = np.max(rot_vel)
    y_max_rot_acc_value = np.max(rot_acc)

    # Create Spider figure
    plt.style.use("seaborn-darkgrid")
    fig, ax = plt.subplots(1, 1, figsize=[10, 6])
    if mirror is True:
        ax.text(0.8, 3.1, 'Endtime: ' + str(round(len(time) / sfreq, 2)) + 's',
                bbox=dict(facecolor='green', alpha=0.5))
    else:
        ax.text(2.7, 6, 'Endtime: ' + str(round(len(time) / sfreq, 2)) + 's',
                bbox=dict(facecolor='green', alpha=0.5))
    ax.plot(-dist_y, dist_x)
    ax.plot(-rot_vel_y_45, rot_vel_x_45, 'y.', markersize=5,
            label='Rot vel > 45 deg/s')
    ax.plot(-rot_vel_y_90, rot_vel_x_90, 'g.', markersize=8,
            label='Rot vel > 90 deg/s')
    ax.plot(-rot_vel_y_180, rot_vel_x_180, 'r.', markersize=14,
            label='Rot vel > 180 deg/s')
    ax.plot(-dist_y[y_max_rot_vel],
            dist_x[y_max_rot_vel], 'ko', markersize=10,
            label='Rot vel$_{peak}:$ ' + str(int(y_max_rot_vel_value)) + ' deg/s')
    ax.plot(-dist_y[y_max_rot_acc],
            dist_x[y_max_rot_acc], 'k*', markersize=10,
            label='Rot acc$_{peak}:$ ' + str(int(y_max_rot_acc_value)) + ' deg/s$^{2}$')
    ax.set_xlabel("Distance [m]", fontsize=12)
    ax.set_ylabel("Distance [m]", fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.set_title(f"{name} Illinois test")
    ax.legend(loc='lower right', prop={'size': 10})

    return ax


def overview_illinois_plot(data, name='', mirror=False):
    """
    Plot spider test

    Parameters
    ----------
    data : pd.Series
        processed illinois pd.Series
    name : str
        name of a session
    mirror : bool
        make true if test is executed in reversed order
    Returns
    -------
    ax: axis object

    """
    vel = "vel"

    vel = data[vel]
    time = data['time']
    dist = data['dist']
    rot_vel = data['rot_vel']

    sfreq = 1 / time.diff().mean()

    # Calculate processed acceleration from velocity
    acc = lowpass_butter(np.gradient(vel) * sfreq, sfreq=sfreq, cutoff=10)

    # Calculate distance in x and y direction
    dist_y = cumtrapz(
        np.gradient(dist) * np.sin(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)
    dist_x = cumtrapz(
        np.gradient(dist) * np.cos(np.deg2rad(cumtrapz(rot_vel / sfreq, initial=0.0))),
        initial=0.0)

    # Change signal if test was executed in reversed order
    if mirror is True:
        dist_x = -dist_x
        dist_y = -dist_y

    # Calculate rotational vel zones and rot_vel_peak, rot_acc_peak
    rot_vel.reset_index(inplace=True, drop=True)
    rot_vel_y_45 = dist_y[rot_vel.abs() > 45]
    rot_vel_x_45 = dist_x[rot_vel.abs() > 45]
    rot_vel_y_90 = dist_y[rot_vel.abs() > 90]
    rot_vel_x_90 = dist_x[rot_vel.abs() > 90]
    rot_vel_y_180 = dist_y[rot_vel.abs() > 180]
    rot_vel_x_180 = dist_x[rot_vel.abs() > 180]
    rot_acc = np.gradient(rot_vel) * sfreq
    y_max_rot_vel = rot_vel.idxmax()
    y_max_rot_acc = np.argmax(rot_acc)
    y_max_rot_vel_value = np.max(rot_vel)
    y_max_rot_acc_value = np.max(rot_acc)
    y_max_vel = vel.idxmax()
    y_max_acc = acc.argmax()
    y_max_vel_value = np.max(vel)
    y_max_acc_value = np.max(acc)

    # Create time vs. rotational velocity figure
    plt.style.use("seaborn-whitegrid")
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=[14, 10])
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    fig.suptitle(f"{name} Overview Illinois test")
    ax1.set_ylim(np.min(rot_vel) - 10, np.max(rot_vel) + 10)
    ax1.plot(time, rot_vel, 'b')
    ax1.set_xlabel("Time [s]", fontsize=10)
    ax1.set_ylabel("Rotational velocity [deg/s]", fontsize=10)
    ax1.tick_params(axis='y', colors='b', labelsize=10)
    ax1.tick_params(axis='x', labelsize=10)
    ax1.yaxis.label.set_color('b')
    ax1.autoscale(axis='x', tight=True)

    # Create time vs. velocity figure with vel_peak
    ax2.set_ylim(0, y_max_vel_value + 0.5)
    ax2.plot(time, vel, 'r')
    ax2.plot(time[y_max_vel], vel[y_max_vel], 'k.',
             label='Vel$_{peak}$: ' + str(round(y_max_vel_value, 2)) + ' m/s')
    ax2.set_xlabel("Time [s]", fontsize=10)
    ax2.set_ylabel("Velocity [m/s]", fontsize=10)
    ax2.tick_params(axis='y', colors='r', labelsize=10)
    ax2.tick_params(axis='x', labelsize=10)
    ax2.yaxis.label.set_color('r')
    ax2.legend(loc='lower right', prop={'size': 8})
    ax2.autoscale(axis='x', tight=True)

    # Create time vs. acceleration figure with acc_peak
    ax3.set_ylim(np.min(acc) - 1, y_max_acc_value + 1)
    ax3.plot(time, acc, 'g')
    ax3.plot(time[y_max_acc], acc[y_max_acc], 'k.',
             label='Acc$_{peak}$: ' + str(round(y_max_acc_value, 2)) + ' m/$s^2$')
    ax3.set_xlabel("Time [s]", fontsize=10)
    ax3.set_ylabel("Acceleration [m/$s^2$]", fontsize=10)
    ax3.tick_params(axis='y', colors='g', labelsize=10)
    ax3.tick_params(axis='x', labelsize=10)
    ax3.yaxis.label.set_color('g')
    ax3.legend(loc='lower center', prop={'size': 10})
    ax3.autoscale(axis='x', tight=True)

    # Create Spider figure
    ax4.text(2.7, 6, 'Endtime: ' + str(round(len(time) / sfreq, 2)) + 's',
             bbox=dict(facecolor='green', alpha=0.5))
    ax4.plot(-dist_y, dist_x)
    ax4.plot(-rot_vel_y_45, rot_vel_x_45, 'y.', markersize=5,
             label='rot_vel > 45 deg/s')
    ax4.plot(-rot_vel_y_90, rot_vel_x_90, 'g.', markersize=8,
             label='rot_vel > 90 deg/s')
    ax4.plot(-rot_vel_y_180, rot_vel_x_180, 'r.', markersize=14,
             label='rot_vel > 180 deg/s')
    ax4.plot(-dist_y[y_max_rot_vel],
             dist_x[y_max_rot_vel], 'ko', markersize=10,
             label='rot_$vel_{peak}$: ' + str(int(y_max_rot_vel_value)) + ' deg/s')
    ax4.plot(-dist_y[y_max_rot_acc],
             dist_x[y_max_rot_acc], 'k*', markersize=10,
             label='rot_$acc_{peak}$: ' + str(int(y_max_rot_acc_value)) + ' deg/$s^2$')
    ax4.set_xlabel("Distance [m]", fontsize=10)
    ax4.set_ylabel("Distance [m]", fontsize=10)
    ax4.tick_params(axis='y', labelsize=10)
    ax4.tick_params(axis='x', labelsize=10)
    ax4.legend(loc='lower right', prop={'size': 8})

    return ax1, ax2, ax3, ax4


def imu_push_plot(time, vel, acc_raw, name='', dec=False):
    """
    Plot push detection with IMUs

    Parameters
    ----------
    time : dict
        time structure
    vel : dict
        velocity structure
    acc_raw : dict
        raw acceleration structure
    name : str
        name of a session
    dec : boolean
        set to True if main deceleration should be found

    Returns
    -------
    ax: axis object

    """
    # Calculate push detection with function
    sfreq = 1 / time.diff().mean()
    push_idx, acc_filt, n_pushes, cycle_time, push_freq = push_imu(acc_raw, sfreq)

    # Change signal if the main deceleration values should be found
    if dec is True:
        acc_filt = -acc_filt

    # Calculate processed acceleration from velocity
    acc = lowpass_butter(np.gradient(vel) * sfreq, sfreq=sfreq, cutoff=20)

    # Create time vs. velocity with push detection figure
    plt.style.use("seaborn-darkgrid")
    fig, ax1 = plt.subplots(1, 1, figsize=[10, 6])
    ax1.set_ylim(-6, 6)
    ax1.plot(time, vel, 'r')
    ax1.plot(time[push_idx], vel[push_idx], 'k.', markersize=10)
    ax1.set_xlabel("Time [s]", fontsize=12)
    ax1.set_ylabel("Velocity [m/s]", fontsize=12)
    ax1.tick_params(axis='y', colors='r', labelsize=12)
    ax1.tick_params(axis='x', labelsize=12)
    ax1.yaxis.label.set_color('r')
    ax1.set_title(f"{name} Push detection Sprint test")

    # Create time vs. acceleration with push detection figure
    ax2 = ax1.twinx()
    ax2.set_ylim(-30, 30)
    ax2.plot(time, acc, 'C7', alpha=0.5)
    ax2.plot(time, acc_filt, 'b')
    ax2.plot(time[push_idx], acc_filt[push_idx], 'k.', markersize=10, label="Detected push")
    ax2.set_ylabel("Acceleration [m/$s^2$]", fontsize=12)
    ax2.tick_params(axis='y', colors='b', labelsize=12)
    ax2.yaxis.label.set_color('b')
    ax2.legend(frameon=True, loc='lower right')

    return ax1, ax2
