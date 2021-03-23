import os
import stat

def prepare_exp(SSHHost, SSHPort, REMOTEROOT, optpt):
    f = open("config", 'w')
    f.write("Host benchmark\n")
    f.write("   Hostname %s\n" % SSHHost)
    f.write("   Port %d\n" % SSHPort)
    f.close()


    f = open("run-experiment.sh", 'w')
    f.write("#!/bin/bash\n")
    f.write("set -x\n\n")

    f.write("sshpass -p 'ubuntu' ssh -o stricthostkeychecking=no ubuntu@server -p 22 \"memcached -P memcached.pid > memcached.out 2> memcached.err &\"\n")

    f.write("RESULT=`sshpass -p 'ubuntu' ssh -o stricthostkeychecking=no ubuntu@server -p 22 pidof memcached`\n")

    f.write("sleep 5\n")

    f.write("if [ -z $RESULT ]; then echo \"memcached process not running\"; CODE=1; else CODE=0; fi\n")

    f.write("%s/mcperf --num-calls=%d --call-rate=%d --num-conns=%d --server=%s > stats.log 2>&1\n\n" % (REMOTEROOT, optpt["noRequests"], optpt["noRequests"], optpt["concurrency"], SSHHost)) #adjust this line to properly start the client

    f.write("LATENCY=$(sed -n 's/Response time \[ms\]: avg \([0-9]\+\.\?[0-9]*\).*$/\\1/p' stats.log)\n")
    f.write("REQPERSEC=$(sed -n 's/Request rate: \([0-9]\+\.\?[0-9]*\).*$/\\1/p' stats.log)\n")

    f.write("sshpass -p 'ubuntu' ssh -o stricthostkeychecking=no ubuntu@server -p 22 \"sudo kill -9 $(cat memcached.pid)\"\n")

    f.write("echo \"requests latency\" > stats.csv\n")
    f.write("echo \"$REQPERSEC $LATENCY\" >> stats.csv\n")

    f.write("sshpass -p 'ubuntu' scp -o stricthostkeychecking=no ubuntu@server:~/memcached.* .\n")

    f.write("if [ $(wc -l <stats.csv) -lt 2 ]; then CODE=1; fi\n\n")

    f.write("exit $CODE\n")

    f.close()

    os.chmod("run-experiment.sh", stat.S_IRWXU)
