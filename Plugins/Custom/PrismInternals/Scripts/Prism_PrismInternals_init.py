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
# This file is part of Prism-Plugin-PrismInternals.
#
# Prism-Plugin-PrismInternals is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


from Prism_PrismInternals_Variables import Prism_PrismInternals_Variables
from Prism_PrismInternals_Functions import Prism_PrismInternals_Functions


class Prism_PrismInternals(Prism_PrismInternals_Variables, Prism_PrismInternals_Functions):
    def __init__(self, core):
        Prism_PrismInternals_Variables.__init__(self, core, self)
        Prism_PrismInternals_Functions.__init__(self, core, self)
