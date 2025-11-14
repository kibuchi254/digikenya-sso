# Official Nginx Alpine (small & secure)
FROM nginx:alpine

# Install certbot + dependencies for auto-renewal
RUN apk add --no-cache \
    certbot \
    certbot-nginx \
    openssl \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom configs
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Create directories for Let's Encrypt
RUN mkdir -p /var/www/certbot /etc/letsencrypt

# Create script for certificate renewal
COPY renew-certs.sh /usr/local/bin/renew-certs.sh
RUN chmod +x /usr/local/bin/renew-certs.sh

# Expose ports
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost/.well-known/acme-challenge/test || exit 1

# Start nginx + auto-renew certs in background
CMD ["/bin/sh", "-c", "renew-certs.sh & nginx -g 'daemon off;'"]