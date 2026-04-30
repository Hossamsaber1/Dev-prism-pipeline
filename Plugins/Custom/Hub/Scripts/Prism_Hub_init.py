# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under proprietary license. See license file in the directory of this plugin for details.
#
# This file is part of Prism-Plugin-Hub.
#
# Prism-Plugin-Hub is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


from Prism_Hub_Variables import Prism_Hub_Variables
from Prism_Hub_Functions import Prism_Hub_Functions


class Prism_Hub(Prism_Hub_Variables, Prism_Hub_Functions):
    def __init__(self, core):
        Prism_Hub_Variables.__init__(self, core, self)
        Prism_Hub_Functions.__init__(self, core, self)
