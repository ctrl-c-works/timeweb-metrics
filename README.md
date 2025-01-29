# How to start

1. Fill config.yaml
    ```shell
    cp ./config.example.yaml ./config.yaml
    vim ./config.yaml
    ```
2. Launch application using **one of two** options
    - in docker
        ```shell
        docker compose up
        ```
    - on host
        ```shell
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        uvicorn app.main:app --reload
        ```
