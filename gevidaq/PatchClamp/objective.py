# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 10:18:47 2021

@author: TvdrBurgt
"""

import importlib.resources
import logging

from pipython import GCSDevice, pitools

from .. import PI_ObjectiveMotor


class PIMotor:
    """Physik Intrumente Objective motor control
    The objective is attached to a motor that can move it up and down. This
    file is a minimalistic version of xinmeng's 'focuser.py' but contains the
    exact same functionality.
    """

    def __init__(self, objective_motor_handle=None):
        # Connect the objective motor if it is not given
        if objective_motor_handle is None:
            files = importlib.resources.files(PI_ObjectiveMotor)
            traversable = files.joinpath("PI_GCS2_DLL_x64.dll")
            with importlib.resources.as_file(traversable) as path:
                self.objective = GCSDevice(gcsdll=str(path))
            self.objective.ConnectUSB(
                serialnum="PI C-863 Mercury SN 0185500828"
            )  # TODO magic string
        else:
            self.objective = objective_motor_handle

    def disconnect(self):
        """
        Disconnects the objective motor, initialization necessary to use it
        again.
        """
        self.objective.CloseConnection()

    def moveAbs(self, z):
        """
        Moves the objective motor to a target position, 'z' is the position
        on the z-axis in millimeters. Example:
            z = 3.45 moves the objective 3.45 millimeters above zero.
        """
        self.objective.MOV(self.objective.axes, z)
        pitools.waitontarget(self.objective)

        # below this line is not really necessary
        positions = self.objective.qPOS(self.objective.axes)
        for axis in self.objective.axes:
            logging.info(
                "position of axis {} = {:.5f}".format(axis, positions[axis])
            )

    def getPos(self):
        """
        Reports the position of the objective motor in units of 10 micron.
        Example:
            position = 3.45 means the motor position is 3.45 millimeters from 0
        """
        positions = self.objective.qPOS(self.objective.axes)

        return positions["1"]
