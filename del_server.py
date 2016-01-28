#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, pyrax, time, warnings
import options

warnings.filterwarnings('ignore')

server_name=options.server_name

pyrax.set_setting('identity_type', 'rackspace')

try:
    pyrax.set_credential_file(os.path.expanduser('~/.rackspace_cloud_credentials'))
except exc.AuthenticationFailed:
    print '''Did you remember to replace the credential file 
             with your actual username and api_key?'''

cs = pyrax.cloudservers
imgs = pyrax.images

for img in imgs.list(visibility='private'):
    if img.name == server_name + '_daily_delete':
        old_image = img
        old_image.change_name(server_name + '_d_d_backup')

server_id = cs.servers.find(name=server_name)

image_name = server_name + '_daily_delete'
image_id = cs.servers.create_image(server_id, image_name) 
time.sleep(5)

for img in imgs.list(visibility='private'):
    if image_id == img.id:
        image = img

pyrax.utils.wait_until(image, "status", "active", interval=30, attempts=1000, verbose=False)

if image.status == 'active':
    server_id.delete()
    try:
        old_image
    except:
        old_image = None
    if old_image != None:
        imgs.delete(old_image)
