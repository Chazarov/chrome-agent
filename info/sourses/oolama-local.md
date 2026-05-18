**Ollama как движок инференса LLM (DevOps-перспектива).**

Ollama — это **open-source runtime** (на Go + llama.cpp backend), оптимизированный для локального инференса quantized GGUF-моделей (Q4_0, Q8_0, FP16). Автоматизирует загрузку, квантизацию, GPU-offload (CUDA/ROCm/Metal) и serving через HTTP API. [habr](https://habr.com/ru/articles/951962/)

**Архитектура:**
- **Core**: llama.cpp (C++) для inference, поддержка multi-modal (LLaVA), tools/functions, embeddings.
- **Modelfile**: YAML-подобный DSL для кастомных моделей (system prompt, params: temp, top_p/k, ctx_size до 128k).
- **API**: OpenAI-compatible (/v1/chat/completions) + native (/api/generate, /api/chat).
- **Storage**: ~/.ollama/models (blobs + manifests), registry с 1000+ моделями. [skillbox](https://skillbox.ru/media/code/ollama/)

**Ключевые метрики (на RTX 4090):**
| Модель | Params | VRAM | Tokens/s |
|--------|--------|------|-----------|
| Llama3.2 | 3B     | 2GB  | 150+     |
| Mistral  | 7B     | 5GB  | 120      |
| Llama3.1 | 70B Q4 | 40GB | 30       |  [habr](https://habr.com/ru/articles/951962/)

**Docker-deploy:**
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --gpus all ollama/ollama
docker exec ollama ollama serve
curl http://localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"Hi"}'
```
Масштаб: Kubernetes с GPU-operator, load-balancer. [oblako](https://oblako.kz/iaas-blog/ollama)

**LangChain**: `ChatOllama(model="llama3.2", temperature=0.1, num_ctx=8192)`. Идеален для on-prem RAG/agents без vendor-lock. [habr](https://habr.com/ru/articles/951962/)


---------------------------------------------------
---------------------------------------------------
---------------------------------------------------
---------------------------------------------------
---------------------------------------------------



**Ollama** — open-source платформа для локального запуска LLM (Llama, Mistral, Gemma, DeepSeek) на ПК/сервере без облака. [tecnoloblog](https://www.tecnoloblog.com/ru/que-es-ollama/)

**Ключевые фичи:**
- CLI + REST API (порт 11434, OpenAI-совместимый)
- Работает на CPU/GPU, Windows/Linux/macOS/Docker
- Библиотека 100+ оптимизированных моделей
- Полная приватность данных [mosregdata](https://mosregdata.ru/article/ollama-introduction-and-quick-start)

**Установка (Linux):**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2  # скачивает модель
ollama run llama3.2   # запускает чат
```

**Для кода LangChain:** `ChatOllama(model="llama3.2", base_url="http://localhost:11434")` [habr](https://habr.com/ru/articles/951962/)
Идеально для DevOps — Docker образ, минимум зависимостей.