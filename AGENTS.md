# ollama

Ejemplos en Python para usar modelos locales de Ollama: un agente con agno, un agente con búsqueda web (DuckDuckGo), un cliente OpenAI-compatible y llamadas a herramientas "a mano" con el cliente de Ollama.

## Visibilidad y rama

- Público. Rama por defecto: `master`.

## Stack

- Python (sin versión fijada).
- `requirements.txt`: `ollama`, `openai~=1.65.2`, `duckduckgo-search`, `agno`.
- Imports usados en `tools_raw.py` y no listados en `requirements.txt`: `geocoder`, `requests`, `pydantic` (no verificado si son necesarios en el entorno).

## Estructura

- `agent.py`: agente agno con `Ollama` (`qwen2.5-coder:3b`) que genera código Python.
- `tools.py`: agente agno con `DuckDuckGoTools` (`qwen2.5:latest`) para responder con información de la web.
- `ollama2openai.py`: cliente `openai` apuntando a `http://localhost:11434/v1` (`qwen2.5-coder:1.5b`).
- `tools_raw.py`: tool calling sin framework con el paquete `ollama` (`llama3.1:latest`); tools `get_time` (hora por zona horaria) y `get_coor` (coordenadas de una ciudad con `geocoder`, usa la variable `PROXY`).
- `requirements.txt`: dependencias.
- `README.md`: enlace a la documentación de agno.
- `.gitignore`: `.idea` y `.venv`.

## Comandos

- Crear entorno e instalar: `python -m venv .venv` y `pip install -r requirements.txt` (no verificado).
- Ejecutar: `python agent.py`, `python tools.py`, `python ollama2openai.py`, `python tools_raw.py`.
- Requisito: servidor de Ollama en `localhost:11434` con los modelos ya descargados (`ollama pull <modelo>`); no verificado.
- Tests: no hay.

## Configuración

- Servidor Ollama en `localhost:11434` (fijo en el código).
- `PROXY` (opcional): proxy para `get_coor` en `tools_raw.py`.
- No hay ficheros de configuración ni secretos. `api_key='ollama'` en `ollama2openai.py` es un valor ficticio que exige el cliente OpenAI, no una clave real.

## Convenciones para agentes

- Mantener cada script autocontenido, sin frameworks nuevos salvo que se pida.
- Modelos fijados en cada script: si se cambian, cambiarlos en el mismo fichero y documentarlo aquí.
- No añadir claves de API ni proxies con credenciales al código.

## Estado

- Sin tests ni CI.
- `tools_raw.py`: `get_time` tiene `@lru_cache` sobre la zona horaria, así que devuelve siempre la misma hora para la misma zona: está cacheado de forma incorrecta para una función que depende del tiempo.
- `tools_raw.py`: en el `except` de `get_time`, `tz` no está asignada y `repr(tz)` fallaría (UnboundLocalError) (probable, por lectura del código).
- `tools_raw.py`: `from pydantic import json` no es el uso habitual (probable error; no verificado).
- `tools.py`: los ejemplos usan `OpenAIChat` en comentarios sin importarlo.
- Los comentarios y la pregunta de ejemplo están en inglés; el resto del repo está en inglés también.
