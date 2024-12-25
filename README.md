# masters-degree-project
This is the public repository for my master's degree thesis/project.
The project is about improving retrieval quality using sentence decomposition and composition according to some specific semantic algebra rules.
This repository allows the reproduction of the experiments that were shown in the thesis, more specifically the comparison between a regular and a modified RAG chain.
The modified RAG chain is a RAG chain that has been modified to include the behaviour decomposition and composition rules, meaning that only the behaviours are indexed and retrieved.

## To reproduce:
- Nvidia GPU required.
### Reproducing locally
#### Pre-requisites
- Python 3.10 or higher should be installed, virtual environment created and activated inside the project directory.
- Makefile should be installed.
- For Windows: Visual studio 2022 with Desktop development with C++ option should be installed.
- For Linux: `build-essential` should be installed.
- Nvidia CUDA Toolkit should be installed.
#### Steps
- Running the `make` or `make start-locally` command will install the necessary dependencies and start a local llm server.
- To reproduce the experiments locally, execute the jupyter notebooks found in the `masters-degree-project/notebooks`.
- Optional: To only restart the server without building or downloading the dependencies, use `make start-llm-server`.
### Reproducing using Docker
#### Pre-requisites
- Docker should be installed.
- Nvidia Container Toolkit should be installed.
#### Steps
- Running the `make start-docker` command will build the docker image and start the llm server.
- The rag_api server's documentation should be accessible at `http://localhost:8086/docs`.
- To reproduce the experiments, use the `/v1/rag_response`, `/v1/modified_rag_response`, and `/v1/init_modified_rag` endpoints to compare the regular and modified rag chains.
- Warning: To use the `/v1/modified_rag_response` endpoint, the `/v1/init_modified_rag` endpoint should be called first. This is because the modified rag model is not loaded by default, and indexing it takes time.
### Note
- In both cases, the LLAMA-CPP server should be available at `http://localhost:8085`.
- Find the server's documentation at `http://localhost:8085/docs`.
- The server's api key should be inside the `.env` file.
