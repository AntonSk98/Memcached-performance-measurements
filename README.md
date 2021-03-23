### Task Description ###
1. There are two docker images that run Memcached and Memcached-benchmark client, ‘dude’ and R
2. Using ‘dude’ the experiment is created that measures throughput and latency for Memcached requests
3. Xyplot is generated using R that shows the measurement performance

##### Container #1: #####
* Base image: Ubuntu 16.04 LTS
* SSH Server – expose port to external port 20022
* Add the CI's public ssh key (gitlab_id_rsa.pub) in addition to yours to the ssh server
* Ssh with public key should work
* Install memcached v1.4.33 (build from source)
* Expose ports for SSH Server and memcached (for other container)
* Run container as user Ubuntu (id=1000) instead of root

##### Container #2: #####
* Base image: Ubuntu 16.04 LTS
* SSH Server – expose port to external port 10022
* Add the CI's public ssh key (gitlab_id_rsa.pub) in addition to yours to the ssh server
* Ssh with public key should work
* Install memcached benchmark client (mcperf)
* Intstall Dude & R
* Run container as user Ubuntu (id=1000) instead of root


##### Docker compose #####
* Docker compose is used to get the communication between the containers running as well as the experiment.

##### The experiment script/work flow #####
* ```dude run```:
* ssh to the memcached server (container #1) to launch memcached
* Launch the benchmark client (locally - container #2)
* Grab the output from the benchmark client: "Response rate", "Response time [ms] avg" - Dude dimensions: rate 
* ```dude sum```: summarizes the output - single csv file
* The plot the graphs ```$ Rscript ….R```

To test it, use the following command sequence:
```
#!/bin/bash

sudo docker-compose up -d
ssh ubuntu@127.0.0.1 -p 10022 "./run.sh"
scp -P 10022 ubuntu@127.0.0.1:~/graph*.pdf .
evince graph*.pdf
sudo docker-compose down
``
