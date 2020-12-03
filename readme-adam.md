(ENV3) pi@red:~ $ sudo apt-get update
Get:1 http://archive.raspberrypi.org/debian buster InRelease [32.6 kB]
Get:2 http://raspbian.raspberrypi.org/raspbian buster InRelease [15.0 kB]
Get:3 http://raspbian.raspberrypi.org/raspbian buster/main armhf Packages [13.0 MB]
Get:4 http://archive.raspberrypi.org/debian buster/main armhf Packages [335 kB]
Fetched 13.4 MB in 30s (450 kB/s)                                                                                    
Reading package lists... Done

(ENV3) pi@red:~ $ sudo apt-get upgrade


(ENV3) pi@red:~ $ sudo cat /var/lib/rancher/k3s/server/node-token
K10126aaacd0a2d1e093900147d64ff9fd68a1663c779c17811fbca9d6f1b31de30::server:c980296a842c92143b6b97d5368d65a9

(ENV3) pi@red:~ $ hostname -I
169.254.144.52 10.6.0.186 

(ENV3) pi@red:~ $ ssh pi@red001.local

pi@red001:~ $ curl -sfL https://get.k3s.io | \
  K3S_URL="https://169.254.144.52:6443" \
  K3S_TOKEN=K10126aaacd0a2d1e093900147d64ff9fd68a1663c779c17811fbca9d6f1b31de30::server:c980296a842c92143b6b97d5368d65a9 \
  sh -

pi@red001:~ $ exit

(ENV3) pi@red:~ $ sudo kubectl get nodes

NAME   STATUS   ROLES    AGE   VERSION
red    Ready    master   9d    v1.19.3+k3s3

worker nodes are not showing up





