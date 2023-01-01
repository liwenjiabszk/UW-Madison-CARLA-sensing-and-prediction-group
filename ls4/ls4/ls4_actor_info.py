import glob
import os
import sys

from cv2 import waitKey
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

import random
import time
import numpy as np
import pandas as pd
import math
import cv2

VEH_NUM = 5
information = []
vehicle_list = []

try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(30.0)
    world = client.get_world()

    blueprint_library = world.get_blueprint_library() 
    vehicle_bp = random.choice(blueprint_library.filter('vehicle.*.*'))

    spawn_points = world.get_map().get_spawn_points()

    for i in range(VEH_NUM):

        vehicle_bp_i = random.choice(blueprint_library.filter('vehicle.*.*'))
        spawn_point_i = spawn_points[i]

        vehicle_i = world.spawn_actor(vehicle_bp_i, spawn_point_i)

        vehicle_i.set_autopilot(True)

        vehicle_list.append(vehicle_i)

    world_snapshot = world.get_snapshot()
    cur_t = world_snapshot.timestamp.elapsed_seconds

    while True:
        world_snapshot = world.get_snapshot()
        frame = world_snapshot.frame
        timestamp = world_snapshot.timestamp.elapsed_seconds


        for i in range(len(vehicle_list)):
            INFO = []
            INFO.append(frame)
            INFO.append(timestamp)
            actor_i = vehicle_list[i]
            loc = actor_i.get_location()
            vel = actor_i.get_velocity()
            acc = actor_i.get_acceleration()

            INFO.append(i)
            INFO.append(loc.x)
            INFO.append(loc.y)
            INFO.append(vel.x)
            INFO.append(vel.y)
            INFO.append(acc.x)
            INFO.append(acc.y)
            information.append(INFO)

        column=['Frame', 'Timestamp', 'Vehicle_ID', 'Location_X', 'Location_Y', 'Velocity_X', 'Velocity_Y','Acceleration_X', 'Acceleration_Y']
        if round(abs(timestamp - cur_t), 1) == 0.1:
            actor_info = pd.DataFrame(columns=column,data=information)
            actor_info.to_csv('C:/Users/liwen/Desktop/ls4/actor_info.csv')
            cur_t = timestamp



    time.sleep(30)


finally:
    print('destroying actors')
    for actor in vehicle_list:
        actor.destroy()
    print('done.')