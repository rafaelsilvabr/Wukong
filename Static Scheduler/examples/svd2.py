import pickle 
import sys

import numpy as np
import pprint

import dask 
import dask.array as da
import time 

#####################################
# SVD of a "Tall-and-Skinny" Matrix #
#####################################

# NOTES:
# - These scripts use the `wukong-config.yaml` file located in "/home/ec2-user/Wukong/Static Scheduler/wukong-config.yaml".
#   Please modify the `wukong_config_path` key-word argument passed to the `LocalCluster` instance on line 37 if your
#   configuration file is located somewhere else. 
#
# - Assuming you're just running this from the cloned repository without installing any Python modules...
#   If you're running this script from somewhere else, then you'll need to modify this import statement.
#   Something like: 
#       from wukong import Client, LocalCluster
sys.path.append("..")
from wukong import Client, LocalCluster
from dask import delayed 
import logging 

lc = LocalCluster(
  host="10.0.88.131:8786",
  proxy_address = "10.0.88.131",
  proxy_port = 8989,
  num_lambda_invokers = 4,
  chunk_large_tasks = False,
  n_workers = 0,
  use_local_proxy = True,
  wukong_config_path = "/home/ec2-user/Wukong/Static Scheduler/wukong-config.yaml",
  local_proxy_path = "/home/ec2-user/Wukong/KV Store Proxy/proxy.py",
  redis_endpoints = [("127.0.0.1", 6379)],
  use_fargate = False)
client = Client(lc)

# Compute the SVD of 'Tall-and-Skinny' Matrix 
X = da.random.random((10000, 10000), chunks=(2000, 2000))
u, s, v = da.linalg.svd_compressed(X, k=5)

# Start the computation.
result = v.compute(scheduler = client.get)
print("Result: %s" % result) 

lc.close()

# If after running this script, there are some lingering Python processes, 
# you can use the following command to terminate the instances. 
# 
# kill -9 $(ps aux | grep '[p]ython3' | awk '{print $2}')