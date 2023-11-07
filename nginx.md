```
sudo apt update

sudo apt install nginx

sudo systemctl start nginx

sudo systemctl enable nginx


server {
    listen 80;
    server_name 192.168.29.18;

    location / {
        proxy_pass http://192.168.29.18:8000;  # Forward requests to your Django app running on port 8000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://192.168.29.18:8000;  # Use the http protocol for WebSocket
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}


sudo nginx -t


sudo systemctl reload nginx
```


Memcache

sudo apt-get install memcached


```bash
 pip install pymemcache
```

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',  # Adjust this to match your Memcached server's address and port
    }
}
