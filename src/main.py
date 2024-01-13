# MIT License
#
# Copyright (c) 2024 Yunus Ruzmetov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pygame_screen_record import ScreenRecorder # Module created by Rashid Harvey (@theRealProHacker on github)
import pygame
import json
import logging
from utils import *
import math
import time
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename="log.log")

def inform(msg, exception, exit_code=1):
    print("\n",msg,"\nMore info on exception can be found in log file.")
    logging.error(msg=f"Exception that caused exit of the application:\n{str(exception)}")
    sys.exit(exit_code)

CONFIG_FILE_NAME = "config.json"
pygame.init()
try:
    config_file = json.load(open(CONFIG_FILE_NAME, "r"))
    logging.info(msg=f"Selected config file {CONFIG_FILE_NAME}")
except Exception as e:
    inform(f"Error while reading file {CONFIG_FILE_NAME}", e)

config = config_file['config']
SCREEN_SIZE = tuple(config["screen_size"])
TIME_SCALE = config["time_scale"]
FPS = config["fps"]
SAVE_FILE = "solar_system.mp4"

circle_center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Planet Simulation")
distance_font = pygame.font.SysFont("JetBrains Mono", 20)
month_font = pygame.font.SysFont("JetBrains Mono", 40)
debug = True

try:
    recorder = ScreenRecorder(FPS)
    recorder.start_rec()
    logging.info(msg="Started recording simulation.")
except Exception as e:
    inform("Error while starting recorder", e)

black = (0, 0, 0)

sun_radius = config["sun_radius"]
sun_color = tuple(config["sun_color"])

planets = config_file["planets"]

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

            data["angle"] += data["angular_speed"]

            distance_text = distance_font.render(f"{int((distance/data['distance_scale'])/1000000)}*10^6 km", True, data["color"])
            if debug:screen.blit(distance_text, (x + 50, y - 50))
        month_text = month_font.render(f"Month: {current_month} Year: {current_year}", True, (255, 255, 255))
        if debug:screen.blit(month_text, (0, 0))

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

finally:
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