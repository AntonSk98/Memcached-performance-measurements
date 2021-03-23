FROM ubuntu:16.04
      
MAINTAINER Anton Skripin(Russia) <anton.skripin@mailbox.tu-dresden.de>

RUN apt-get update
RUN apt-get upgrade -y

#variables
ARG MY_PUBLIC_KEY='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2g/M4f2fGbIa89MgZORH2O2IJs0h5fE7fcbUTvlySi6Yv0F9f2iW0fE0gvWXv58YLds7hjv65LtIMBXEJuVw+iUH8/c9KcUJpyzqfR+dSzO4E7pxWCDjfR+1lOF8tndPTXqX84ADDOn1XI08T1UO9rKPGVzMtqoTu7aK/+pKbPr7k1H/+3s4tomp2mQJnPesQzBTf8K6YTojAxDpl1U7tAjvqDTd7RxfBeANeo0Jf0YhQ62yRcrRDJEyoQ2uD46LQJRaQyDOyW6Qb8todWHRxSRnIeJnIukgiVtgJug5yObzuoMAWllTMuI4TIVc3RQiB/f0ImOl7WLkXfgmWT5F1 antonsk98@DESKTOP-CLBAP8B'
ARG GITLAB_MACHINE_PUBLIC_KEY='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcFj9AJ0yx2NswwEKPFQZqpiYZ8Mzk1LlRNatsVQqUfaDoQTKewuHRpp5jREB9RIMPczgFPDZSOBQ+mV8u5qJScmOcB8rhaF0GZkF1KIgHSNj8VqDNZWP52m1+NxSJetp6Opu3zTzkoZt9uo4HHeVZseTfN0UkxSjcWKYPX7+rOrvMhIxxKB9bR7UjmMkmoMfzP8UVkmc4MxIOo+RW9OM9GFselGN9JTYceZW8xhWNH2ENXQNWE5a807vP6kaKWp5bQ/c7NpISvTAO5UaVD26IRrtqea//MiUORjbXX+dEpFZuN6fRMh+zemerQ9rDHcgxRMacGZxBUjIRCa92zSr3 gitlab-runner@sep'

#sudo and openssh-server install
RUN apt-get install -y sudo
RUN apt-get install -y openssh-server

# set up ubuntu user
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 ubuntu
RUN echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
# provide public keys
RUN mkdir /var/run/sshd
RUN mkdir home/ubuntu/.ssh
RUN echo $GITLAB_MACHINE_PUBLIC_KEY >> home/ubuntu/.ssh/authorized_keys
RUN echo $MY_PUBLIC_KEY >> home/ubuntu/.ssh/authorized_keys


# install sshpass to set_up config
RUN apt-get install -y sshpass
# install mcperf
RUN apt-get install -y build-essential
WORKDIR /mcperf
ARG MCPERF_PATH='https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/twemperf/mcperf-0.1.1.tar.gz'
RUN wget $MCPERF_PATH
RUN tar -zxf mcperf-0.1.1.tar.gz
RUN ./mcperf-0.1.1/configure
RUN cd mcperf-0.1.1
RUN make -f Makefile
RUN make install
# install R
RUN apt-get install -y software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial/'
RUN apt-get install -y apt-transport-https ca-certificates
RUN apt-get update
RUN apt-get install -y r-base
# install Python 2
WORKDIR /python2
RUN apt-get update
RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
RUN wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz
RUN tar -zxf Python-2.7.18.tgz
RUN ./Python-2.7.18/configure --enable-optimizations
RUN make altinstall
#install dude
WORKDIR /dude
RUN apt install -y git
RUN git clone https://bitbucket.org/db7/dude.git
WORKDIR /dude/dude
RUN python setup.py install
RUN python setup.py install --home=$HOME/local
RUN export PATH=$PATH:$HOME/local/bin
RUN export PYTHONPATH=$PYTHONPATH:$HOME/local/lib/python

#expose default port for ssh
USER ubuntu
RUN sudo mkdir ~/.ssh/known_hosts
RUN sudo chown -v ubuntu ~/.ssh/known_hosts
EXPOSE 22
#copy script to run it via ssh
COPY run.sh /home/ubuntu/
WORKDIR /home/ubuntu/
RUN sudo chmod +x run.sh
#copy Benchmark and Dudefile
COPY Benchmark.py /home/ubuntu/
COPY Dudefile /home/ubuntu/
COPY graphs.R /home/ubuntu/
RUN sudo apt install -y nano
RUN cp /usr/local/bin/mcperf /home/ubuntu/mcperf

#as soon as the container starts ssh to the server to start memcached and run ssh server
CMD sudo /usr/sbin/sshd -D