FROM ubuntu:24.04

ENV PYTHONUNBUFFERED=1

RUN apt-get update --yes --quiet &&  DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    software-properties-common build-essential curl apt-utils \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository universe && apt-get update --yes --quiet

RUN DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    python3 \
    python3-dev \
    python3-venv \
    pip

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONPATH "${PYTHONPATH}:/opt/"

WORKDIR /opt

RUN pip install uv
COPY ./requirements/rag-api.requirements.txt requirements/rag-api.requirements.txt
RUN uv pip install -r requirements/rag-api.requirements.txt

COPY masters_degree_project masters_degree_project
EXPOSE 8086
CMD ["uvicorn", "masters_degree_project.entrypoints.rag_api:app", "--host", "localhost", "--port", "8086"]
