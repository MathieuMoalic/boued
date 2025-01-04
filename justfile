staging:
    podman build -t localhost/groceries-staging:latest .

    podman run -d --replace \
        --name groceries-staging \
        --network tmp-proxy \
        -v .dev/data:/data:z \
        localhost/groceries-staging:latest