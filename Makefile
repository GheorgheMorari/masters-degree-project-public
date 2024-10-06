build-llm-server:
	@ echo "Building local llm server..."
	@ pip install llama-cpp-python[server] --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu125
	@ echo "Building local llm server... Done"

start-llm-server:
	@ echo "Starting local llm server..."
	@ python -m llama_cpp.server --config_file ./llama_cpp/server_config.json

download-phi3-mini-128k-model:
	@ echo "Downloading phi3 mini 128k model..."
	@ mkdir -p ./llama_cpp/models/phi3_mini_128k_model
	@ rm -f ./llama_cpp/models/phi3_mini_128k_model/phi3_mini_128k_model.gguf
	@ wget https://huggingface.co/PrunaAI/Phi-3-mini-128k-instruct-GGUF-Imatrix-smashed/resolve/main/Phi-3-mini-128k-instruct.Q4_K_M.gguf?download=true -O ./llama_cpp/models/phi3_mini_128k_model/phi3_mini_128k_model.gguf

download-mixedbread-embed-model:
	@ echo "Downloading mixedbread embed model..."
	@ mkdir -p ./llama_cpp/models/mixedbread
	@ rm -f ./llama_cpp/models/mixedbread/mxbai-embed-large-v1-f16.gguf
	@ wget https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1/resolve/main/gguf/mxbai-embed-large-v1-f16.gguf?download=true -O ./llama_cpp/models/mixedbread/mxbai-embed-large-v1-f16.gguf
