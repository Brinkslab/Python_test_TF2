# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 18:21:18 2021

@author: tvdrb
"""


import os
import datetime
import logging
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

from PatchClamp.workers import Worker


class SmartPatcher(QObject):
    
    def __init__(self):
        # Algorithm constants
        self._pipette_orientation = None                     # in radians
        self._pipette_diameter = None                        # in microns
        self._pipette_coordinates = np.array([None, None])   # [X, Y] in pixels
        self._target_coordinates = np.array([None, None])    # [X, Y] in pixels
        
        # Hardware devices
        self._camerathread = None
        self._amplifierthread = None
        self._pressurethread = None
        self._micromanipulator = None
        self._objectivemotor = None
        
        # Worker thread
        self.worker = Worker()
        # self.thread = QThread()
        # self.worker.moveToThread(self.thread)
    
    @property
    def camerathread(self):
        return self._camerathread
    
    @camerathread.setter
    def camerathread(self, camerathread_handle):
        self._camerathread = camerathread_handle
        self._camerathread.start()
    
    @camerathread.deleter
    def camerathread(self):
        self._camerathread.stop()
        self._camerathread = None
    
    def set_amplifierthread(self, patchamplifier):
        self.amplifierthread = patchamplifier
    
    def set_pressurethread(self, pressurecontroller):
        self.pressurethread = pressurecontroller
        
        
    @property
    def micromanipulator(self):
        return self._micromanipulator
    
    @micromanipulator.setter
    def micromanipulator(self, micromanipulator_handle):
        self._micromanipulator = micromanipulator_handle
    
    @micromanipulator.deleter
    def micromanipulator(self):
        self._micromanipulator.stop()
        self._micromanipulator.close()
        self._micromanipulator = None
        
        
    def set_objectivemotor(self, objective):
        self.objectivemotor = objective
    
    
    @property
    def pipette_orientation(self):
        return self._pipette_orientation
    
    @pipette_orientation.setter
    def pipette_orientation(self, angle):
        logging.info('Set pipette orientation: \phi =' + str(angle))
        if type(angle) == float or type(angle) == int:
            self._pipette_orientation = angle
        else:
            raise ValueError('micromanipulator orientation should be a float or integer')
    
    @pipette_orientation.deleter
    def pipette_orientation(self):
        self._pipette_orientation = None
    
    
    @property
    def pipette_diameter(self):
        return self._pipette_diameter
    
    @pipette_diameter.setter
    def pipette_diameter(self, diameter):
        logging.info('Set pipette opening diameter: D =' + str(diameter))
        if type(diameter) == float or type(diameter) == int:
            self._pipette_diameter = diameter
        else:
            raise ValueError('Pipette opening diameter should be a float or integer')
    
    @pipette_diameter.deleter
    def pipette_diameter(self):
        self._pipette_diameter = None
    
    
    @property
    def pipette_coordinates(self):
        return self._pipette_coordinates
    
    @pipette_coordinates.setter
    def pipette_coordinates(self, coords):
        logging.info('Set pipette coordinates: [x,y,z]=' + str(coords))
        if type(coords) is np.ndarray:
            if len(coords) == 2:
                self._pipette_coordinates = coords
            else:
                raise ValueError('length of pipette coordinates must be 2 or 3')
        else:
            raise ValueError('pipette coordinates should be a numpy.ndarray')
    
    @pipette_coordinates.deleter
    def pipette_coordinates(self):
        self._pipette_coordinates = np.array([None, None])
    
    
    @property
    def target_coordinates(self):
        return self._target_coordinates
    
    @target_coordinates.setter
    def target_coordinates(self, coords):
        logging.info('Set target coordinates: [x,y,z]=' + str(coords))
        if type(coords) is np.ndarray:
            if len(coords) == 2:
                self._target_coordinates = coords
            else:
                raise ValueError('length of target coordinates must be 2 or 3')
        else:
            raise ValueError('target coordinates should be a numpy.ndarray')
    
    @target_coordinates.deleter
    def target_coordinates(self):
        self._pipette_coordinates = np.array([None, None])
    
    