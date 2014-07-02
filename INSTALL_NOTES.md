1. Install haproxy

```
sudo apt-get install haproxy
sudo vim /etc/default/haproxy # change ENABLED=0 to ENABLED=1
```

2. Add a config file

```
mv /etc/haproxy/haproxy.cfg{,.original}
cp haproxy.cfg /etc/haproxy/haproxy.cfg
```

3. Run the server

```
nohup ./wsgi.py script args >stdout.log 2>stderr.log&
```

