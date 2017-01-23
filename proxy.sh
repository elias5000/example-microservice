#/bin/bash
sed -i "s/__env_port__/$PORT/g" /etc/nginx/conf.d/proxy.conf
sed -i "s/__env_upstream__/$UPSTREAM/g" /etc/nginx/conf.d/proxy.conf

nginx \
  -g "daemon off; error_log /dev/stdout info;"
