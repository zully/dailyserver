#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, pyrax, time, sys, warnings
import options

warnings.filterwarnings('ignore')

server_name=options.server_name
domain_name=options.domain_name

host_name=server_name + '.' + domain_name

pyrax.set_setting('identity_type', 'rackspace')
pyrax.set_setting('region', 'IAD')

try:
    pyrax.set_credential_file(os.path.expanduser('~/.rackspace_cloud_credentials'))
except pyrax.exc.AuthenticationFailed:
    print '''Did you remember to replace the credential file 
             with your actual username and api_key?'''

cs = pyrax.cloudservers
imgs = pyrax.images
dns = pyrax.cloud_dns

try:
    cs.servers.find(name=server_name)
    found = True
except:
    found = False

if found:
    print 'Server %s already exists!' % server_name
    sys.exit(1)

flavor_id = 'performance1-1'

for img in imgs.list(visibility='private'):
    if img.name == server_name + '_daily_delete':
        image_id = img.id

server = cs.servers.create(server_name, image_id, flavor_id)
time.sleep(30)

pyrax.utils.wait_until(server, "status", "ACTIVE", interval=10, attempts=1000, verbose=False)

for v in server.networks['public']:
    if '.' in v:
        ip = v

try:
    dom = dns.find(name=domain_name)
except pyrax.exc.NotFound:
    print "Unable to find domain by that name: " + domain_name
    raise SystemExit

try:
    recs = dom.list_records()
except:
    print "Unable to list records!"
    raise SystemExit

for rec in recs:
    if rec.name == host_name:
        try:
            rec.update(data=ip)
        except:
            print "Unable to update record!"
            raise SystemExit
