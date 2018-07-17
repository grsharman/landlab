import os

import pytest
import numpy as np

from landlab import RasterModelGrid
from landlab import BAD_INDEX_VALUE as XX
from landlab.components.flow_routing import (
    FlowRouter, DepressionFinderAndRouter,
)


@pytest.fixture
def dans_grid1():
    """
    Create a 5x5 test grid.
    This is a sheet flow test.
    """
    # global fr, mg, infile
    # global z, Q_in, A_target, frcvr_target, upids_target, Q_target, \
    #     steepest_target, links2rcvr_target

    mg = RasterModelGrid((5, 5), spacing=(10., 10.))

    this_dir = os.path.abspath(os.path.dirname(__file__))
    infile = os.path.join(this_dir, 'test_fr_input.txt')

    z = mg.node_x.copy()

    Q_in = np.full(25, 2.)

    A_target = np.array([0.,  0.,  0.,  0.,  0.,
                         3.,  3.,  2.,  1.,  0.,
                         3.,  3.,  2.,  1.,  0.,
                         3.,  3.,  2.,  1.,  0.,
                         0.,  0.,  0.,  0.,  0.])*100.

    frcvr_target = np.array([0,  1,  2,  3,  4,
                             5,  5,  6,  7,  9,
                            10, 10, 11, 12, 14,
                            15, 15, 16, 17, 19,
                            20, 21, 22, 23, 24])

    upids_target = np.array([0,  1,  2,  3,  4,
                             5,  6,  7,  8,  9,
                            10, 11, 12, 13, 14,
                            15, 16, 17, 18, 19,
                            20, 21, 22, 23, 24])

    links2rcvr_target = np.full(25, XX)
    links2rcvr_target[mg.core_nodes] = np.array([ 9, 10, 11,
                                                 18, 19, 20,
                                                 27, 28, 29])

    Q_target = A_target * 2.  # only once Q_in is used

    steepest_target = np.array([0.,  0.,  0.,  0.,  0.,
                                0.,  1.,  1.,  1.,  0.,
                                0.,  1.,  1.,  1.,  0.,
                                0.,  1.,  1.,  1.,  0.,
                                0.,  0.,  0.,  0.,  0.])

    mg.add_field('node', 'topographic__elevation', z, units='-')

    class DansGrid(object):
        pass

    dans_grid = DansGrid()
    dans_grid.mg = mg
    dans_grid.z = z
    dans_grid.infile = infile
    dans_grid.A_target = A_target
    dans_grid.frcvr_target = frcvr_target
    dans_grid.upids_target = upids_target
    dans_grid.Q_target = Q_target
    dans_grid.steepest_target = steepest_target
    dans_grid.links2rcvr_target = links2rcvr_target

    return dans_grid


@pytest.fixture
def dans_grid2():
    """
    Create a 5x5 test grid.
    This tests more complex routing, with diffs between D4 & D8.
    """
    mg = RasterModelGrid((5, 5), spacing=(10., 10.))

    this_dir = os.path.abspath(os.path.dirname(__file__))
    infile = os.path.join(this_dir, 'test_fr_input.txt')

    z = np.array([7.,  7.,  7.,  7.,  7.,
                  7.,  5., 3.2,  6.,  7.,
                  7.,  2.,  3.,  5.,  7.,
                  7.,  1., 1.9,  4.,  7.,
                  7.,  0.,  7.,  7.,  7.])

    A_target_D8 = np.array([0.,     0.,     0.,     0.,     0.,
                            0.,   100.,   200.,   100.,     0.,
                            0.,   400.,   100.,   100.,     0.,
                            0.,   600.,   300.,   100.,     0.,
                            0.,   900.,     0.,     0.,     0.])

    A_target_D4 = np.array([0.,     0.,     0.,     0.,     0.,
                            0.,   100.,   200.,   100.,     0.,
                            0.,   200.,   400.,   100.,     0.,
                            0.,   900.,   600.,   100.,     0.,
                            0.,   900.,     0.,     0.,     0.])

    frcvr_target_D8 = np.array([0, 1, 2, 3, 4, 5, 11, 11, 7, 9, 10, 16, 16, 17,
                                14, 15, 21, 21, 17, 19, 20, 21, 22, 23, 24])

    frcvr_target_D4 = np.array([ 0,  1,  2,  3,  4, 
                                 5, 11, 12,  7,  9,
                                10, 16, 17, 12, 14,
                                15, 21, 16, 17, 19,
                                20, 21, 22, 23, 24])

    upids_target_D8 = np.array([0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21,
                                16, 11, 6, 7, 8, 12, 17, 13, 18, 22, 23, 24])

    upids_target_D4 = np.array([0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21,
                                16, 11, 6, 17, 12, 7, 8, 13, 18, 22, 23, 24])

    links2rcvr_target_D8 = np.full(25, XX)
    links2rcvr_target_D8[mg.core_nodes] = np.array([14, 51, 11,
                                                    23, 59, 61,
                                                    32, 67, 29])

    links2rcvr_target_D4 = np.full(25, XX)
    links2rcvr_target_D4[mg.core_nodes] = np.array([14, 15, 11,
                                                    23, 24, 20,
                                                    32, 28, 29])

    steepest_target_D8 = np.array([0., 0., 0., 0., 0.,
                                   0., 0.3, 0.08485281, 0.28, 0.,
                                   0., 0.1, 0.14142136, 0.21920310, 0.,
                                   0., 0.1, 0.13435029, 0.21,  0.,
                                   0., 0., 0., 0.,  0.])

    steepest_target_D4 = np.array([0., 0., 0., 0., 0.,
                                   0., 0.3, 0.02, 0.28, 0.,
                                   0., 0.1, 0.11, 0.2, 0.,
                                   0., 0.1, 0.09, 0.21, 0.,
                                   0., 0., 0., 0., 0.])

    mg.add_field('node', 'topographic__elevation', z, units='-')


    # global fr, mg, infile
    # global z, A_target_D8, A_target_D4, frcvr_target_D8, frcvr_target_D4, \
    #     upids_target_D8, upids_target_D4, steepest_target_D8, \
    #     steepest_target_D4, links2rcvr_target_D8, links2rcvr_target_D4

    class DansGrid(object):
        pass

    dans_grid = DansGrid()
    dans_grid.mg = mg
    dans_grid.z = z
    dans_grid.infile = infile
    dans_grid.A_target_D8 = A_target_D8
    dans_grid.A_target_D4 = A_target_D4
    dans_grid.frcvr_target_D8 = frcvr_target_D8
    dans_grid.frcvr_target_D4 = frcvr_target_D4
    dans_grid.upids_target_D8 = upids_target_D8
    dans_grid.upids_target_D4 = upids_target_D4
    dans_grid.steepest_target_D8 = steepest_target_D8
    dans_grid.steepest_target_D4 = steepest_target_D4
    dans_grid.links2rcvr_target_D8 = links2rcvr_target_D8
    dans_grid.links2rcvr_target_D4 = links2rcvr_target_D4

    return dans_grid


@pytest.fixture
def d4_grid():
    """Test functionality of routing when D4 is specified.

    The elevation field in this test looks like::

    1   2   3   4   5   6   7

    1   2   3   0   5   0   7

    1   2   3   4   0   0   7

    1   2   3   0   5   6   7

    1   2   0   0   0   6   7

    1   2   3   0   5   6   7

    1   2   3   4   5   6   7
    """
    mg1 = RasterModelGrid(7, 7, 1.)
    mg2 = RasterModelGrid(7, 7, 1.)
    z = mg1.node_x.copy() + 1.
    lake_nodes = np.array([10, 16, 17, 18, 24, 32, 33, 38, 40])
    z[lake_nodes] = 0.
    mg1.add_field('node', 'topographic__elevation', z, units='-')
    mg2.add_field('node', 'topographic__elevation', z, units='-')

    frD8 = FlowRouter(mg1, method='D8')
    frD4 = FlowRouter(mg2, method='D4')
    lfD8 = DepressionFinderAndRouter(mg1, routing='D8')
    lfD4 = DepressionFinderAndRouter(mg2, routing='D4')

    class DansGrid(object):
        pass

    d4_grid = DansGrid()
    d4_grid.mg1 = mg1
    d4_grid.mg2 = mg2
    d4_grid.z = z
    d4_grid.lake_nodes = lake_nodes
    d4_grid.frD8 = frD8
    d4_grid.frD4 = frD4
    d4_grid.lfD8 = lfD8
    d4_grid.lfD4 = lfD4

    return d4_grid
