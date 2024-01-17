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
# The full veresion of the script can be found in the COPYING file.
# You should have received a copy of the GNU General Public License
# along with Planet Simulation.  If not, see <http://www.gnu.org/licenses/>.

import logging
import sys

LOGFILE = "log.log"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=LOGFILE)

def inform(msg, exception, exit_code=1):
    print("\n",msg,"\nMore info on exception can be found in log file.")
    logging.error(msg=f"Exception that caused exit of the application:\n{str(exception)}")
    sys.exit(exit_code)

try:
    from pygame_screen_record import ScreenRecorder # Module created by Rashid Harvey (@theRealProHacker on github)
    from xlsxwriter import Workbook
    import pygame
    import json
    from utils import *
    import argparse
    import csv
    from statistics import mean
    import math
    import time
except ModuleNotFoundError as e:
    inform("Run `pip3 install -r requirements.txt` to installed required libraries.", e)

parser = argparse.ArgumentParser(description='Simulate the orbit of the 8 planets in our solar system.')
parser.add_argument('--output-type', choices=['csv', 'json', 'xlsx'], default='json', help='The output file/data type.')
parser.add_argument('--output-file', default='output', help='The output filename without the extension.')
parser.add_argument("--screen-size", required=False, help="The size of the window in pixels (1280x720)")
parser.add_argument("--text-font", required=False, help="The font of the text on the window")
parser.add_argument('--verbose', default='1', choices=['0', '1', '2'], help='Verbosity level of the simulation')
args = parser.parse_args()


CONFIG_FILE_NAME = "config.json"
try:
    config_file = json.load(open(CONFIG_FILE_NAME, "r"))
    logging.info(msg=f"Selected config file {CONFIG_FILE_NAME}")
except Exception as e:
    inform(f"Error while reading file {CONFIG_FILE_NAME}", e)
try:
    config = config_file['config']
except KeyError as e:
    inform("Missing config file keys.", e)

if not args.screen_size:
    SCREEN_SIZE = tuple(config["screen_size"])
else:
    SCREEN_SIZE = tuple([int(i) for i in str(args.screen_size).split("x")])
    print(SCREEN_SIZE)
try:
    TIME_SCALE = config["time_scale"]
    FPS = config["fps"]
    SAVE_FILE = "solar_system.mp4"
except KeyError as e:
    inform("Missing keys in config file.", e)


pygame.init()

with open(LOGFILE, "w") as f:
    f.write("")

circle_center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Planet Simulation")
distance_font = pygame.font.SysFont("JetBrains Mono", 20)
month_font = pygame.font.SysFont("JetBrains Mono", 40)

debug = int(args.verbose)
try:
    recorder = ScreenRecorder(FPS)
    recorder.start_rec()
    logging.info(msg="Started recording simulation.")
except Exception as e:
    inform("Error while starting recorder", e)

black = (0, 0, 0)

try:
    sun_radius = config["sun_radius"]
    sun_color = tuple(config["sun_color"])
except KeyError as e:
    inform("Missing keys in config file.", e)

try:
    planets = config_file["planets"]
except KeyError as e:
    inform("Missing planet key in config file.")

orbit_counts = {planet: 0 for planet in planets}
planet_distances = {planet: [] for planet in planets}
planet_speeds = {planet: [] for planet in planets}
mean_distances = {planet: 0 for planet in planets}
mean_speeds = {planet: 0 for planet in planets}
output_data = []

start = time.time()
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info(msg="Exiting program")
                pygame.quit()
                sys.exit(0)
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                if pygame.display.is_fullscreen():
                    screen = pygame.display.set_mode(SCREEN_SIZE)
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        screen.fill(black)

        end = time.time()
        duration = (end-start)*TIME_SCALE
        current_month, current_year = day_month(duration,1)
        pygame.draw.circle(screen, sun_color, circle_center, sun_radius)
        for planet, data in planets.items():
            m_radius = data["radius"] / data["distance_scale"]
            rps_angular_velocity = data["angular_speed"] * FPS
            mps_velocity = m_radius*rps_angular_velocity
            planet_speeds[planet].append(float(mps_velocity))
            if data["angle"] >= 2 * math.pi:
                data["angle"] = 0
                orbit_counts[planet] += 1
            pygame.draw.ellipse(screen, (255, 255, 255), (circle_center[0] - data["semi_major_axis"],
                                                        circle_center[1] - data["semi_minor_axis"],
                                                        data["semi_major_axis"] * 2,
                                                        data["semi_minor_axis"] * 2), width=1)
            x = int(circle_center[0] + data["semi_major_axis"] * math.cos(data["angle"]))
            y = int(circle_center[1] + data["semi_minor_axis"] * math.sin(data["angle"]))

            pygame.draw.circle(screen, data["color"], (x, y), data["radius"])
            angle = calc_angle(circle_center, (x, y))
            if debug:pygame.draw.line(screen, data["color"], circle_center, (x, y), 2)

            distance = math.sqrt((x - circle_center[0])**2 + (y - circle_center[1])**2)
            planet_distances[planet].append(distance)

            data["angle"] += data["angular_speed"]
            distance_text = distance_font.render(f"{int((distance/data['distance_scale'])/1000000)}*10^6 km", True, data["color"])
            name_text = distance_font.render(str(planet), True, data["color"])
            angle_text = distance_font.render(str(int(angle))+"°", True, data["color"])
            screen.blit(name_text, (x + 50, y - 50))
            if debug>1:screen.blit(angle_text, (x + 50, y - 10))
            if debug>0:screen.blit(distance_text, (x + 50, y - 30))
        month_text = month_font.render(f"Month: {current_month} Year: {current_year}", True, (255, 255, 255))
        total_orbit = month_font.render(f"Total orbits: {str(int(sum(orbit_counts.values())))}", True, (255, 255, 255))
        if debug>0:screen.blit(month_text, (0, 0))
        if debug>1:screen.blit(total_orbit, (0, 50))

        pygame.display.flip()
        try:
            pygame.time.Clock().tick(FPS)
        except KeyboardInterrupt:
            sys.exit(0)

finally:
    for planet, data in planet_distances.items():
        mean_distances[planet] = mean(data)
    for planet, data in planet_speeds.items():
        mean_speeds[planet] = mean(data)
    for i in planets:
        output_data.append({"name": i, "mean_distance": mean_distances[i], "mean_velocity": mean_speeds[i], "orbit_count": orbit_counts[i]})
    # Store output
    if args.output_type=="json":
        with open(f"{args.output_file}.{args.output_type}", "w") as f:
            json.dump(output_data, f, indent=4)
    elif args.output_type=="csv":
        fieldnames = output_data[0].keys()
        with open(f"{args.output_file}.{args.output_type}", 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(output_data)
    elif args.output_type=="xlsx":
        ordered_list = list(output_data[0].keys())
        wb = Workbook(f"{args.output_file}.{args.output_type}")
        ws = wb.add_worksheet()
        first_row=0
        for header in ordered_list:
            col=ordered_list.index(header)
            ws.write(first_row,col,header)
        # XLSX Code snipped from stackoverflow (user Fatih1923)
        row=1
        for data in output_data:
            for _key,_value in data.items():
                col=ordered_list.index(_key)
                ws.write(row,col,_value)
            row+=1
        wb.close()
    logging.info(msg="Exiting program")
    pygame.quit()
    save_name = SAVE_FILE.split(".")
    try:
        recorder.stop_rec()
        recording = recorder.get_single_recording()
        logging.info(msg="Successfully stopped recording")
    except Exception as e:
        inform("Error while stopping recorder", e)
    try:
        recording.save((save_name[0], save_name[1]))
        logging.info(msg=f"Successfully saved recording into {SAVE_FILE}")
    except Exception as e:
        inform(f"Error while saving recording into {str(SAVE_FILE)}")
    print(f"\nOutput data was written to {args.output_file}.{args.output_type}")