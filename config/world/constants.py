#!/usr/bin/env python
# Author: Kelcey Jamison-Damage
# Python: 2.66 +
# OS: CentOS | Other
# Portable: True
# License: Apache 2.0

# License
#-----------------------------------------------------------------------#
# Copyright [2016] [Kelcey Jamison-Damage]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-----------------------------------------------------------------------#
# Constants
#-----------------------------------------------------------------------#
TILESIZE = 10
MAPWIDTH = 160
MAPHEIGHT = 80
PADDING = 0
HILL = 0 # 30% speed
GRASS = 1 # 100% speed
WATER = 2 # impasable
FOREST = 3 # 60% speed
COAST = 4 # 80% speed
CITY = 5 # 150 # sped
LOWHILL = 8
MOUNTAIN = 9
PLAYER = 6
ROAD = 7 # 150% speed