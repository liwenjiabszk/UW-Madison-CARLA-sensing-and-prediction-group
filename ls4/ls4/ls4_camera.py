import glob
import os
import sys
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
import cv2

IM_WIDTH = 640
IM_HEIGHT = 480

def process_img(image, name):
    print("Frame: "+str(image.frame)+", timestamp: "+str(image.timestamp))
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    cv2.imshow(name, i3)
    cv2.waitKey(1)

    if image.frame % 20 == 0:
        image.save_to_disk('C:/Users/liwen/Desktop/ls4/img/camera%02d.png' % image.frame)
    return i3/255.0


actor_list = []
try:
    client = carla.Client('localhost', 2000) 

    world = client.get_world()

    blueprint_library = world.get_blueprint_library() 

    vehicle_bp = blueprint_library.filter('model3')[0]
    print(vehicle_bp)

    spawn_point = random.choice(world.get_map().get_spawn_points())
    print(spawn_point)

    vehicle = world.spawn_actor(vehicle_bp, spawn_point)


    vehicle.set_autopilot(True) 

    actor_list.append(vehicle)

    
    cam_bp = blueprint_library.find('sensor.camera.rgb')

    cam_bp.set_attribute('image_size_x', f'{IM_WIDTH}')
    cam_bp.set_attribute('image_size_y', f'{IM_HEIGHT}')
    cam_bp.set_attribute('fov', '110')



    spawn_point_cam = carla.Transform(carla.Location(x=2.5, z=1.0))


    camera = world.spawn_actor(cam_bp, spawn_point_cam, attach_to=vehicle)

    actor_list.append(camera)

    camera.listen(lambda data: process_img(data, "camera1"))

    time.sleep(30)

finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')