#!/bin/sh
 python server/server.py 8004
 
 python client/client.py 127.0.0.1 8004
 python node/node.py 8000
