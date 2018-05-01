#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 09:17:36 2018

@author: barnhark
"""

import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
from nose.tools import assert_raises, assert_almost_equal, assert_equal

from landlab import RasterModelGrid
from landlab.layers import RockBlock

def test_no_topographic__elevation():
    """Test init with no topo__elevation."""
    mg = RasterModelGrid(3, 3)
    thicknesses = [1, 2, 4, 1]
    ids = [1, 2, 1, 2]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    assert_raises(ValueError, RockBlock, mg, thicknesses, ids, attrs)
    
    
def test_thickness_ids_wrong_shape():
    """Test wrong size thickness and id shapes."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    assert_raises(ValueError, RockBlock, mg, thicknesses, ids, attrs)
    
    ones = np.ones(mg.number_of_nodes)
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1*ones, 2*ones, 4*ones, 1*ones, 5*ones]
    ids = [1*ones, 2*ones, 1*ones, 2*ones]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    assert_raises(ValueError, RockBlock, mg, thicknesses, ids, attrs)
    
    
def test_thickness_nodes_wrong_shape():
    """Test wrong size thickness and id shapes."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    ones = np.ones(mg.number_of_nodes + 1) 
    thicknesses = [1*ones, 2*ones, 4*ones, 1*ones, 5*ones]
    ids = [1*ones, 2*ones, 1*ones, 2*ones, 1*ones]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}    
    assert_raises(ValueError, RockBlock, mg, thicknesses, ids, attrs)
       
    
def test_init_with_thickness_zero():
    """Test RockBlock with zero thickness on init."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [0, 0, 0, 0]
    ids = [1, 2, 1, 2]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    assert_raises(ValueError, RockBlock, mg, thicknesses, ids, attrs)
    
    
def test_atts_lack_ids():
    """Test RockBlock missing ID."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2]
    attrs = {'K_sp': {2: 0.0001}}
    assert_raises(ValueError, RockBlock, mg, thicknesses, ids, attrs)
    
    
def test_erode_to_zero_thickness():
    """Test that eroding RockBlock to zero thickness raises an error."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2, 1]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    rb = RockBlock(mg, thicknesses, ids, attrs)
    assert_raises(ValueError, rb.add_layer, -100)


def test_deposit_with_no_rock_id():
    """Test that adding a deposit to RockBlock with no id raises an error."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2, 1]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    rb = RockBlock(mg, thicknesses, ids, attrs)
    assert_raises(ValueError, rb.add_layer, 100) 


def test_deposit_with_bad_rock_id():
    """Test that adding a deposit to RockBlock with no id raises an error."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2, 1]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    rb = RockBlock(mg, thicknesses, ids, attrs)
    assert_raises(ValueError, rb.add_layer, 100, rock_id=3) 
        
    ones = np.ones(mg.number_of_nodes)
    new_ids = [0, 1, 3, 4, 0, 1, 0, 1, 5]
    assert_raises(ValueError, rb.add_layer, ones, rock_id=new_ids) 
    
def test_adding_existing_attribute():
    """Test adding an existing attribute."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2, 1]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    rb = RockBlock(mg, thicknesses, ids, attrs)
    
    new_attr = {'K_sp': {1: 0.001, 2: 0.0001}}
    
    assert_raises(ValueError, rb.add_attribute, new_attr) 
        
    
def test_adding_new_attribute_missing_rock_id():
    """Test adding an new attribute missing an existing rock id."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2, 1]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    rb = RockBlock(mg, thicknesses, ids, attrs)
    
    new_attr = {'D': {2: 0.0001}}
    
    assert_raises(ValueError, rb.add_attribute, new_attr) 
    
    
def test_adding_new_attribute_extra_rock_id():
    """Test adding an new attribute with an extra rock id."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2, 1]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    rb = RockBlock(mg, thicknesses, ids, attrs)
    
    new_attr = {'D': {1: 0.001, 2: 0.0001, 3: 5.3}}
    
    assert_raises(ValueError, rb.add_attribute, new_attr) 
        
    
def test_adding_new_id_extra_attribute():
    """Test adding an new rock type with an extra attribute."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2, 1]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    rb = RockBlock(mg, thicknesses, ids, attrs)
    
    new_attr = {'K_sp': {4: 0.001, 5: 0.0001},
                'D':    {4: 0.001, 5: 0.0001}}
    
    assert_raises(ValueError, rb.add_rock_type, new_attr) 
    
def test_adding_new_id_missing_attribute():
    """Test adding an new rock type with an extra attribute."""
    mg = RasterModelGrid(3, 3)
    z = mg.add_zeros('node', 'topographic__elevation')
    thicknesses = [1, 2, 4, 1, 5]
    ids = [1, 2, 1, 2, 1]
    attrs = {'K_sp': {1: 0.001, 2: 0.0001}}
    rb = RockBlock(mg, thicknesses, ids, attrs)
    
    new_attr = {'D':  {4: 0.001, 5: 0.0001}}
    
    assert_raises(ValueError, rb.add_rock_type, new_attr) 