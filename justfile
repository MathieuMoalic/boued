set dotenv-load

d:
    podman build -t localhost/groceries-staging:latest .

    podman run --rm --replace \
        --name groceries-staging \
        --network tmp-proxy \
        -v ./data:/data \
        -p 6001:6001 \
        -e PASSWORD=${GROCERY_PASSWORD} \
        localhost/groceries-staging:latest 
    
it: 
    podman build -t localhost/groceries-staging:latest .

    podman run --rm -it --replace \
        --name groceries-staging \
        --network tmp-proxy \
        -v ./data:/data \
        -p 6001:6001 \
        -e PASSWORD=${GROCERY_PASSWORD} \
        localhost/groceries-staging:latest bash