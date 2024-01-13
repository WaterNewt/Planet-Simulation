# Copyright (C) 2024 Yunus Ruzmetov
# 
# This file is part of Planet Simulation Project.
# 
# Planet Simulation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Planet Simulation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Planet Simulation.  If not, see <http://www.gnu.org/licenses/>.

import math
from datetime import datetime, timedelta

def calc_angle(coord1:tuple|list|set, coord2:tuple|list|set):
    x1, y1 = coord1
    x2, y2 = coord2
    dx = x2 - x1
    dy = y2 - y1
    rads = math.atan2(-dy,dx)
    rads %= 2*math.pi
    degs = math.degrees(rads)
    return degs

def day_month(day_number, starting_year):
    years_elapsed = int(day_number / 365)
    remaining_days = day_number % 365

    start_date = datetime(year=starting_year, month=1, day=1)
    target_date = start_date + timedelta(days=remaining_days)

    year = target_date.year
    month_name = target_date.strftime('%B')

    return month_name, years_elapsed