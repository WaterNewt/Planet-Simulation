<!--
 Copyright (C) 2024 Yunus Ruzmetov
 
 This file is part of Planet Simulation.
 
 Planet Simulation is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 Planet Simulation is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with Planet Simulation.  If not, see <http://www.gnu.org/licenses/>.
-->

# Planet Simulation
[<img src="https://www.gnu.org/graphics/gplv3-or-later-sm.png" width=60></img>](https://www.gnu.org/licenses/gpl-3.0.html)
-
A simple, but cool Python simulation of the 8 planets in our solar system.
This project was inspired by [TechWithTim](https://www.techwithtim.net)

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](.github/CONTRIBUTING.md)
- [Code of Conduct](.github/CODE_OF_CONDUCT.md)
- [License](#license)
- [License File](./COPYING)

## Installation
First, clone the repository

```git clone https://github.com/waternewt/planet-simulation```

`cd` into the directory and then run the bash script with `bash run.sh`
If the bash script fails, you can run it manually by `cd`ing into the `/src` folder and then running `main.py` python script.

## Usage
To get info about the arguments you can type `python3 main.py --help`
### Output
After you exit the pygame window, it will save a json file with the output data. If you instead want to save it into a CSV or an Excel spreadsheet, you can use the `--output-type` argument. For now the only supported datatypes are json/csv/xlsx. You can use the `--output-file` argument to specify the name of the file (without the extension) the data will be saved to. By default (if you don't specify the argument), the output file value will be set to <b>output</b>. Other datatypes may be added in the future.

### Verbosity
There's an argument in the script called `--verbosity`, this is the debug level of the simulation (aka, how much data you will be able to see). The options for verbosity (for now) are just 0, 1 and 2. Verbosity 0 will only show the planets and the orbit shape, verbosity 1 will show the month, the year, the distance from the planet to the sun, the name of the planet and a line from the planet to the center of the sun. Verbosity 2 will additionaly show the angle of the line and the total orbits (of  all the planets) in the top left corner of the window.

## License

Copyright (C) 2024 Yunus Ruzmetov

This program is free software distributed under the terms of the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html).

See the [full license text](./COPYING) for details.

Contact:
- Email: waternewtinfo@gmail.com
- Secondary email: waternewt423@gmail.com