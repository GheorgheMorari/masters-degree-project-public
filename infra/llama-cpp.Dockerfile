FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV PYTHONUNBUFFERED=1

# SYSTEM
RUN apt-get update --yes --quiet &&  DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    software-properties-common build-essential curl apt-utils \
    && rm -rf /var/lib/apt/lists/*

# PYTHON 3.10
RUN add-apt-repository --yes ppa:deadsnakes/ppa && apt-get update --yes --quiet
RUN DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    python3.10-lib2to3 \
    pip

RUN pip install --upgrade pip

ENV PYTHONPATH "${PYTHONPATH}:/opt/"

# LLAMA-CPP
WORKDIR /opt
COPY ./requirements/llama-cpp.requirements.txt requirements/llama-cpp.requirements.txt
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install -r requirements/llama-cpp.requirements.txt --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 --force-reinstall --no-cache-dir

COPY ./llama_cpp ./llama_cpp
EXPOSE 8085
CMD ["python3", "-m", "llama_cpp.server", "--config_file", "./llama_cpp/server_config.json"]
