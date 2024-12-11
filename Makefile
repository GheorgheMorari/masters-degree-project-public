build-llm-server:
	@ echo "Building local llm server..."
	@ CMAKE_ARGS="-DLLAMA_CUBLAS=on"
	@ FORCE_CMAKE=1
	@ pip install uv
	@ uv pip install -r requirements.txt --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 --force-reinstall --no-cache-dir
	@ echo "Building local llm server... Done"

build-llm-server-windows:
	@ echo "Building local llm server..."
	@ pip install uv
	@ set CMAKE_ARGS = "-DLLAMA_CUBLAS=on"
	@ set FORCE_CMAKE=1
	@ uv pip install -r requirements.txt --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 --force-reinstall --no-cache-dir
	@ echo "Building local llm server... Done"

start-llm-server:
	@ echo "Starting local llm server..."
	@ python -m llama_cpp.server --config_file ./llama_cpp/server_config.json

download-phi3-mini-model:
	@ echo "Downloading phi3 mini model..."
	@ mkdir -p ./llama_cpp/models/phi3_mini_model
	@ rm -f ./llama_cpp/models/phi3_mini_model/phi3_mini_model.gguf
	@ wget https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf -O ./llama_cpp/models/phi3_mini_model/phi3_mini_model.gguf

download-mixedbread-embed-model:
	@ echo "Downloading mixedbread embed model..."
	@ mkdir -p ./llama_cpp/models/mixedbread
	@ rm -f ./llama_cpp/models/mixedbread/mxbai-embed-large-v1-f16.gguf
	@ wget https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1/resolve/main/gguf/mxbai-embed-large-v1-f16.gguf?download=true -O ./llama_cpp/models/mixedbread/mxbai-embed-large-v1-f16.gguf
