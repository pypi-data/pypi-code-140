"""
    picasso.clusterer
    ~~~~~~~~~~~~~~~~~

    Clusterer optimized for DNA PAINT in CPU and GPU versions.


    Based on the work of Thomas Schlichthaerle and Susanne Reinhardt.
    :authors: Thomas Schlichthaerle, Susanne Reinhardt, 
        Rafal Kowalewski, 2020-2022
    :copyright: Copyright (c) 2022 Jungmann Lab, MPI of Biochemistry
"""

import os as _os

import numpy as _np
import math as _math
import yaml as _yaml
import pandas as _pd
from scipy.spatial import cKDTree as _cKDTree

from . import lib as _lib

# from icecream import ic

CLUSTER_CENTERS_DTYPE_2D = [
    ("frame", "u4"),
    ("x", "f4"),
    ("y", "f4"),
    ("photons", "f4"),
    ("sx", "f4"),
    ("sy", "f4"),
    ("bg", "f4"),
    ("lpx", "f4"),
    ("lpy", "f4"),
    ("ellipticity", "f4"),
    ("net_gradient", "f4"),
    ("n", "u4"),
] 
CLUSTER_CENTERS_DTYPE_3D = [
    ("frame", "u4"),
    ("x", "f4"),
    ("y", "f4"),
    ("z", "f4"),
    ("photons", "f4"),
    ("sx", "f4"),
    ("sy", "f4"),
    ("bg", "f4"),
    ("lpx", "f4"),
    ("lpy", "f4"),
    ("lpz", "f4"),
    ("ellipticity", "f4"),
    ("net_gradient", "f4"),
    ("n", "u4"),
] # for saving cluster centers# for saving cluster centers


def _frame_analysis(frame, n_frames):
    """
    Verifies which clusters pass basic frame analysis.

    Rejects clusters whose mean frame is outside of the 
    [20, 80] % (max frame) range or any 1/20th of measurement's time
    contains more than 80 % of localizations.

    Assumes frame to be a pandas.SeriesGruopBy object, grouped by
    cluster ids.

    Parameters
    ----------
    frame : pandas.SeriesGruopBy
        Frame number for a given cluster; grouped by cluster ids
    n_frames : int
        Acquisition time given in frames

    Returns
    -------
    int
        1 if passed frame analysis, 0 otheriwse
    """

    passed = 1

    # get mean frame
    mean_frame = frame.values.mean()

    # get maximum number of locs in a 1/20th of acquisition time
    n_locs = len(frame)
    locs_binned = _np.histogram(
        frame.values, bins=_np.linspace(0, n_frames, 21)
    )[0]
    max_locs_bin = locs_binned.max()

    # test if frame analysis passed
    if (
        (mean_frame < 0.2 * n_frames)
        or (mean_frame > 0.8 * n_frames)
        or (max_locs_bin > 0.8 * n_locs)
    ):
        passed = 0

    return passed

def frame_analysis(labels, frame):
    """
    Performs basic frame analysis on clustered localizations.

    Rejects clusters whose mean frame is outside of the 
    [20, 80] % (max frame) range or any 1/20th of measurement's time
    contains more than 80 % of localizations.

    Uses pandas for fast calculations using groupby().

    Parameters
    ----------
    labels : np.array
        Cluster labels (-1 means no cluster assigned)
    frame : np.array
        Frame number for each localization

    Returns
    -------
    np.array
        Cluster labels for each localization (-1 means no cluster 
        assigned)
    """

    # group frames by cluster ids
    frame_pd = _pd.Series(frame, index=labels)
    frame_grouped = frame_pd.groupby(frame_pd.index)

    # perform frame analysis
    true_cluster = frame_grouped.apply(_frame_analysis, frame.max()+1)

    # cluster ids that did not pass frame analysis
    discard = true_cluster.index[true_cluster == 0].values
    # change labels of these clusters to -1
    labels[_np.isin(labels, discard)] = -1

    return labels

def _cluster(X, radius, min_locs, frame):
    """
    Clusters points given by X with a given clustering radius and 
    minimum number of localizaitons withing that radius using KDTree

    Parameters
    ----------
    X : np.array
        Array of points of shape (n_points, n_dim) to be clustered
    radius : float
        Clustering radius
    min_locs : int
        Minimum number of localizations in a cluster
    frame : np.array
        Frame number of each localization. If None, no frame analysis
        is performed

    Returns
    -------
    np.array
        Cluster labels for each localization (-1 means no cluster 
        assigned)
    """

    ## build kdtree (use cKDTree in case user did not update scipy)
    tree = _cKDTree(X)

    ## find neighbors for each point within radius
    neighbors = tree.query_ball_tree(tree, radius)

    ## find local maxima, i.e., points with the most neighbors within
    ## their neighborhood
    lm = _np.zeros(X.shape[0], dtype=_np.int8)
    for i in range(len(lm)):
        idx = neighbors[i] # indeces of points that are neighbors of i
        n = len(idx) # number of neighbors of i
        if n > min_locs: # note that i is included in its neighbors
            # if i has the most neighbors in its neighborhood
            if n == max([len(neighbors[_]) for _ in idx]):
                lm[i] = 1

    ## assign cluster labels to all points (-1 means no cluster)
    ## if two local maxima are within radius from each other, combine
    ## such clusters
    labels = -1 * _np.ones(X.shape[0], dtype=_np.int32) # cluster labels
    lm_idx = _np.where(lm == 1)[0] # indeces of local maxima

    for count, i in enumerate(lm_idx): # for each local maximum
        label = labels[i]
        if label == -1: # if lm not assigned yet
            labels[neighbors[i]] = count
        else:
            # indeces of locs that were not assigned to any cluster
            idx = [
                neighbors[i][_]
                for _ in _np.where(labels[neighbors[i]] == -1)[0]
            ]
            if len(idx): # if such a loc exists, assign it to a cluster
                labels[idx] = label

    if frame is not None:
        labels = frame_analysis(labels, frame)

    return labels

def cluster_2D(x, y, frame, radius, min_locs, fa):
    """
    Prepares 2D input to be used by _cluster()

    Parameters
    ----------
    x : np.array
        x coordinates to be clustered
    y : np.array
        y coordinates to be clustered
    frame : np.array
        Frame number for each localization 
    radius : float
        Clustering radius
    min_locs : int
        Minimum number of localizations in a cluster
    fa : bool
        True, if basic frame analysis is to be performed

    Returns
    -------
    np.array
        Cluster labels for each localization (-1 means no cluster 
        assigned)
    """

    X = _np.stack((x, y)).T

    if not fa:
        frame = None

    labels = _cluster(X, radius, min_locs, frame)

    return labels

def cluster_3D(x, y, z, frame, radius_xy, radius_z, min_locs, fa):
    """
    Prepares 3D input to be used by _cluster()

    Scales z coordinates by radius_xy / radius_z

    Parameters
    ----------
    x : np.array
        x coordinates to be clustered
    y : np.array
        y coordinates to be clustered
    z : np.array
        z coordinates to be clustered
    frame : np.array
        Frame number for each localization 
    radius_xy : float
        Clustering radius in x and y directions
    radius_z : float
        Clutsering radius in z direction
    min_locs : int
        Minimum number of localizations in a cluster
    fa : bool
        True, if basic frame analysis is to be performed

    Returns
    -------
    np.array
        Cluster labels for each localization (-1 means no cluster 
        assigned)
    """

    radius = radius_xy
    X = _np.stack((x, y, z * radius_xy / radius_z)).T

    if not fa:
        frame = None

    labels = _cluster(X, radius, min_locs, frame)
    
    return labels

def cluster(locs, params, pixelsize):
    """
    Clusters localizations given user parameters using KDTree.

    Finds if localizations are 2D or 3D.

    Paramaters
    ----------
    locs : np.recarray
        Localizations to be clustered
    params : tuple
        SMLM clustering parameters
    pixelsize : int
        Camera pixel size in nm

    Returns
    -------
    np.array
        Cluster labels for each localization (-1 means no cluster 
        assigned)
    """

    if hasattr(locs, "z"): # 3D
        radius_xy, radius_z, min_locs, _, fa, _ = params
        labels = cluster_3D(
            locs.x,
            locs.y,
            locs.z / pixelsize, # convert z coordinates from nm to px
            locs.frame,
            radius_xy,
            radius_z,
            min_locs,
            fa
        )
    else:
        radius, min_locs, _, fa, _ = params
        labels = cluster_2D(
            locs.x,
            locs.y,
            locs.frame,
            radius,
            min_locs,
            fa
        )
    return labels

def error_sums_wtd(x, w):
    """ 
    Function used for finding localization precision for cluster 
    centers.

    Parameters
    ----------
    x : float
        x or y coordinate of the cluster center
    w : float
        weight (localization precision squared)

    Returns
    -------
    float
        weighted localizaiton precision of the cluster center
    """

    return (w * (x - (w * x).sum() / w.sum())**2).sum() / w.sum()

def find_cluster_centers(locs):
    """
    Calculates cluster centers. 

    Uses pandas.groupby to quickly run across all cluster ids.

    Parameters
    ----------
    locs : np.recarray
        Clustered localizations (contain group info)

    Returns
    -------
    np.recarray
        Cluster centers saved as localizations
    """

    # group locs by their cluster id (group)
    locs_pd = _pd.DataFrame(locs)
    grouplocs = locs_pd.groupby(locs_pd.group)

    # get cluster centers
    centers_ = grouplocs.apply(cluster_center).values

    # convert to recarray and save
    frame = _np.array([_[0] for _ in centers_])
    x = _np.array([_[1] for _ in centers_])
    y = _np.array([_[2] for _ in centers_])
    photons = _np.array([_[3] for _ in centers_])
    sx = _np.array([_[4] for _ in centers_])
    sy = _np.array([_[5] for _ in centers_])
    bg = _np.array([_[6] for _ in centers_])
    lpx = _np.array([_[7] for _ in centers_])
    lpy = _np.array([_[8] for _ in centers_])
    ellipticity = _np.array([_[9] for _ in centers_])
    net_gradient = _np.array([_[10] for _ in centers_])
    n = _np.array([_[11] for _ in centers_])

    if hasattr(locs, "z"):
        z = _np.array([_[12] for _ in centers_])
        lpz = _np.array([_[13] for _ in centers_])
        centers = _np.rec.array(
            (
                frame,
                x,
                y,
                z,
                photons,
                sx,
                sy,
                bg,
                lpx,
                lpy,
                lpz,
                ellipticity,
                net_gradient,
                n,
            ),
            dtype=CLUSTER_CENTERS_DTYPE_3D,
        )
    else:
        centers = _np.rec.array(
            (
                frame,
                x,
                y,
                photons,
                sx,
                sy,
                bg,
                lpx,
                lpy,
                ellipticity,
                net_gradient,
                n,
            ),
            dtype=CLUSTER_CENTERS_DTYPE_2D,
        )

    if hasattr(locs, "group_input"):
        group_input = _np.array([_[-1] for _ in centers_])
        centers = _lib.append_to_rec(centers, group_input, "group_input")

    return centers

def cluster_center(grouplocs, separate_lp=False):
    """
    Finds cluster centers and their attributes.

    Assumes locs to be a pandas.SeriesGroupBy object, grouped by
    cluster ids.

    Paramaters
    ----------
    grouplocs : pandas.SeriesGroupBy
        Localizations grouped by cluster ids
    separate_lp : bool (default=False)
        If True, localization precision in x and y will be calculated
        separately. Otherwise, the mean of the two is taken
    
    Returns
    -------
    list
        Attributes used for saving the given cluster as .hdf5
        (frame, x, y, etc)
    """

    # mean frame
    frame = grouplocs.frame.mean()
    # average x and y, weighted by lpx, lpy
    x = _np.average(grouplocs.x, weights=1/(grouplocs.lpx)**2)
    y = _np.average(grouplocs.y, weights=1/(grouplocs.lpy)**2)
    # mean values
    photons = grouplocs.photons.mean()
    sx = grouplocs.sx.mean()
    sy = grouplocs.sy.mean()
    bg = grouplocs.bg.mean()
    # weighted mean loc precision
    lpx = _np.sqrt(
        error_sums_wtd(grouplocs.x, grouplocs.lpx)
        / (len(grouplocs) - 1)
    )
    lpy = _np.sqrt(
        error_sums_wtd(grouplocs.y, grouplocs.lpy)
        / (len(grouplocs) - 1)
    )
    if not separate_lp:
        lpx = (lpx + lpy) / 2
        lpy = lpx
    # other attributes
    ellipticity = sx / sy
    net_gradient = grouplocs.net_gradient.mean()
    # n_locs in cluster
    n = len(grouplocs)
    if hasattr(grouplocs, "z"):
        # take lpz = 2 * mean(lpx, lpy)
        z = _np.average(
            grouplocs.z, 
            weights=1/((grouplocs.lpx+grouplocs.lpy)**2),
        )
        lpz = 2 * lpx
        result = [
            frame,
            x,
            y,
            photons,
            sx,
            sy,
            bg,
            lpx,
            lpy,
            ellipticity,
            net_gradient,
            n, 
            z, 
            lpz,
        ]
    else:
        result = [
            frame,
            x,
            y,
            photons,
            sx,
            sy,
            bg,
            lpx,
            lpy,
            ellipticity,
            net_gradient,
            n, 
        ]

    if hasattr(grouplocs, "group_input"):
        # assumes only one group input!
        result.append(_np.unique(grouplocs.group_input)[0]) 
    return result