### Nagles algorithm and efs-utils v2.0.0

### Dependencies
```
$ git clone https://github.com/boto/botocore.git
$ cd botocore
$ virtualenv venv
...
$ . venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
```

### Commands
TLS mount with efs-proxy:
```
sudo mount -t efs -o tls,az=us-east-1b fs-033c3bbf7dafaeb9a:/ efs-proxy
```

TLS mount with stunnel:
```
sudo mount -t efs -o stunnel,az=us-east-1b fs-033c3bbf7dafaeb9a:/ efs-stunnel
```

Packet capture:
```
tcpdump -W 30 -C 1000 -s 2000 -w nfs_pcap_$(date +%FT%T).pcap -i any -z gzip -Z root 'port 2049 or (src 127.0.0.1 and dst 127.0.0.1)'
```