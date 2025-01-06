set dotenv-load

staging:
    podman build -t localhost/groceries-staging:latest .

    podman run --rm --replace \
        --name groceries-staging \
        --network tmp-proxy \
        -v ./data:/data \
        -p 6001:6001 \
        -e PASSWORD=${GROCERY_PASSWORD} \
        localhost/groceries-staging:latest 
    
caddy:
    podman run --rm -d --replace \
        --name caddy \
        --network tmp-proxy \
        -v ./Caddyfile:/etc/caddy/Caddyfile \
        -p 80:80 \
        -p 443:443 \
        caddy:latest

backend:
    DATABASE_URL=sqlite:///./test.db \
    ADMIN_USERNAME=${ADMIN_USERNAME} \
    ADMIN_PASSWORD=${ADMIN_PASSWORD} \
    uvicorn backend.main:app --proxy-headers --host 0.0.0.0 --port 6001 --reload