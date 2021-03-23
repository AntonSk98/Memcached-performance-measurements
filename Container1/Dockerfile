FROM ubuntu:16.04

MAINTAINER Anton Skripin(Russia) <anton.skripin@mailbox.tu-dresden.de>

#variables
ARG MY_PUBLIC_KEY='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2g/M4f2fGbIa89MgZORH2O2IJs0h5fE7fcbUTvlySi6Yv0F9f2iW0fE0gvWXv58YLds7hjv65LtIMBXEJuVw+iUH8/c9KcUJpyzqfR+dSzO4E7pxWCDjfR+1lOF8tndPTXqX84ADDOn1XI08T1UO9rKPGVzMtqoTu7aK/+pKbPr7k1H/+3s4tomp2mQJnPesQzBTf8K6YTojAxDpl1U7tAjvqDTd7RxfBeANeo0Jf0YhQ62yRcrRDJEyoQ2uD46LQJRaQyDOyW6Qb8todWHRxSRnIeJnIukgiVtgJug5yObzuoMAWllTMuI4TIVc3RQiB/f0ImOl7WLkXfgmWT5F1 antonsk98@DESKTOP-CLBAP8B'
ARG GITLAB_MACHINE_PUBLIC_KEY='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcFj9AJ0yx2NswwEKPFQZqpiYZ8Mzk1LlRNatsVQqUfaDoQTKewuHRpp5jREB9RIMPczgFPDZSOBQ+mV8u5qJScmOcB8rhaF0GZkF1KIgHSNj8VqDNZWP52m1+NxSJetp6Opu3zTzkoZt9uo4HHeVZseTfN0UkxSjcWKYPX7+rOrvMhIxxKB9bR7UjmMkmoMfzP8UVkmc4MxIOo+RW9OM9GFselGN9JTYceZW8xhWNH2ENXQNWE5a807vP6kaKWp5bQ/c7NpISvTAO5UaVD26IRrtqea//MiUORjbXX+dEpFZuN6fRMh+zemerQ9rDHcgxRMacGZxBUjIRCa92zSr3 gitlab-runner@sep'

#system update/upgrate
RUN apt-get update
RUN apt-get upgrade -y

#sudo and openssh-server install
RUN apt-get install -y sudo
RUN apt-get install -y openssh-server

# set up ubuntu user
RUN adduser --disabled-password --gecos '' --uid 1000 ubuntu
RUN adduser ubuntu sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'ubuntu:ubuntu' | chpasswd

# provide public keys
RUN mkdir /var/run/sshd
RUN mkdir home/ubuntu/.ssh
RUN echo $GITLAB_MACHINE_PUBLIC_KEY >> home/ubuntu/.ssh/authorized_keys
RUN echo $MY_PUBLIC_KEY >> home/ubuntu/.ssh/authorized_keys

#delete access rights for group and others
RUN chmod -R go= home/ubuntu/.ssh
#assign the directory to ubuntu user
RUN chown -R ubuntu home/ubuntu/.ssh

#installing memcached
RUN apt-get install -y build-essential
RUN apt-get install -y libevent-dev
WORKDIR /memcached
RUN wget https://memcached.org/latest
RUN tar -zxf latest
RUN ./memcached-*/configure
RUN cd memcached-*
RUN make -f Makefile
RUN make install
#copy to ssh root to start up memcached on ssh
RUN cp /usr/local/bin/memcached /home/ubuntu/memcached
#run container as user ubuntu
USER ubuntu

EXPOSE 22 11211
CMD ["sudo", "/usr/sbin/sshd", "-D"]