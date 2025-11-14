#!/bin/bash
# renew-certs.sh - Runs in background, renews certs automatically

echo "Starting Let's Encrypt auto-renewal service..."

while true; do
    echo "[$(date)] Checking for certificate renewal..."
    certbot renew --webroot -w /var/www/certbot --quiet
    
    # Reload nginx gracefully after renewal
    if [ $? -eq 0 ]; then
        echo "[$(date)] Certificates renewed successfully. Reloading nginx..."
        nginx -s reload
    else
        echo "[$(date)] No renewal needed."
    fi

    # Sleep 12 hours
    sleep 12h
done