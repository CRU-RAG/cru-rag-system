# CRU-RAG

## Websocket tester:
Clik here to access a websocket tester.
[CRU-RAG](https://piehost.com/websocket-tester)


Brief description about the project goes here

## Manage docker containers

1. Building docker containers

    ```bash
    docker-compose build
    ```

2. Starting docker containers

    ```bash
   docker-compose up
    ```
   or
    ```bash
   docker-compose up -d
    ```
3. Checking docker containers status

    ```bash
   docker-compose ps
    ```

4. Stopping docker containers 

    ```bash
   docker-compose down
    ```

5. Stopping docker containers

    ```bash
   docker-compose exec -it container-name bash
    ```
   Example: 

   ```bash
   docker-compose exec -it rag-server bash
    ```

## Code quality and formatting

1. Running pylint: Pylint analyzes your code for potential errors and enforces coding standards. To run Pylint, use the following command:

    ```bash
    pylint test.py
    pylint .
    ```

2. Running Black: Black is an opinionated code formatter that ensures your code adheres to a consistent style. To format code with Black, use the following command:

    ```bash
    black test.py
    black .
    ```
