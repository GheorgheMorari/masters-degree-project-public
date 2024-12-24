start-locally: build-llm-server download-phi3-mini-model download-mixedbread-embed-model start-llm-server

build-llm-server:
	@ echo "Building local llm server..."
ifeq ($(VIRTUAL_ENV),)
	@echo "Error: Must be in a virtual environment to run this script."
	@exit 1
endif

ifeq ($(OS),Windows_NT)
	@ set CMAKE_ARGS="-DLLAMA_CUBLAS=on"
	@ set FORCE_CMAKE=1
else
	@ CMAKE_ARGS="-DLLAMA_CUBLAS=on"
	@ FORCE_CMAKE=1
endif
	@ pip install uv
	@ uv pip install -r requirements/llama-cpp.requirements.txt --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 --force-reinstall --no-cache-dir
	@ uv pip install -r requirements/requirements.txt
	@ echo "Building local llm server... Done"

download-phi3-mini-model:
	@ echo "Downloading phi3 mini model..."
ifeq ($(OS),Windows_NT)
	@ mkdir -p .\llama_cpp\models\phi3_mini_model 2>nul || exit 0
	@ del /f /q .\llama_cpp\models\phi3_mini_model\phi3_mini_model.gguf 2>nul || exit 0
else
	@ mkdir -p ./llama_cpp/models/phi3_mini_model
	@ rm -f ./llama_cpp/models/phi3_mini_model/phi3_mini_model.gguf
endif
	@ curl -L -o ./llama_cpp/models/phi3_mini_model/phi3_mini_model.gguf https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf
	@ echo "Downloading phi3 mini model... Done"

download-mixedbread-embed-model:
	@ echo "Downloading mixedbread embed model..."
ifeq ($(OS),Windows_NT)
	@ mkdir -p .\llama_cpp\models\mixedbread 2>nul || exit 0
	@ del /f /q .\llama_cpp\models\mixedbread\mxbai-embed-large-v1-f16.gguf 2>nul || exit 0
else
	@ mkdir -p ./llama_cpp/models/mixedbread
	@ rm -f ./llama_cpp/models/mixedbread/mxbai-embed-large-v1-f16.gguf
endif
	@ curl -L -o ./llama_cpp/models/mixedbread/mxbai-embed-large-v1-f16.gguf https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1/resolve/main/gguf/mxbai-embed-large-v1-f16.gguf?download=true

start-llm-server:
	@ echo "Starting local llm server..."
	@ python -m llama_cpp.server --config_file ./llama_cpp/server_config.json
