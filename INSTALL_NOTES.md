Here's how to set up a long-running instance of bookshrink on your own server:

1. Install `haproxy`

```bash
sudo apt-get install haproxy
sudo vim /etc/default/haproxy # change ENABLED=0 to ENABLED=1
```

2. Install the `haproxy` config file

```bash
sudo mv /etc/haproxy/haproxy.cfg{,.original}
sudo cp haproxy.cfg /etc/haproxy/haproxy.cfg
```

3. Turn on `haproxy` and set up a daemonized bookshrink process.

```
sudo service haproxy start
make prod
```

Now visit your server on port 80!
