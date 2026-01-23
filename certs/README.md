
# generate certs for site on Internet

See <https://physicsderivationgraph.blogspot.com/2021/10/periodic-renewal-of-https-letsencrypt.html>

# how to generate local certificates

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out fullchain.pem -keyout privkey.pem -days 365
openssl dhparam -out dhparam.pem 2048
```
