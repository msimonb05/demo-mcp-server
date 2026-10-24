# Demo MCP Server

A small Python MCP server built with the official MCP Python SDK. It demonstrates registering tools and exposing them over SSE, including an addition function, a random-number generator, and a simple weather lookup.

This project was created following the ideas in [How to Build Your Own MCP Server with Python](https://www.freecodecamp.org/news/how-to-build-your-own-mcp-server-with-python/), with updates to use the `MCPServer` API.

## Tools

| Tool | Inputs | Description |
| :--- | :--- | :--- |
| `add` | `num1` (int), `num2` (int) | Adds two integers. |
| `randomizer` | `start` (int), `end` (int) | Chooses a pseudorandom integer from the range `[start, end)`. The `end` value is exclusive. |
| `get_weather_info` | `city` (str) | Fetches weather information for a city from [wttr.in](https://wttr.in/). Requires an internet connection. |

## Tech Stack

| Category | Technology |
| :--- | :--- |
| Language | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| Containerization | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |
| MCP SDK | `mcp` |
| Transport | SSE |
| MCP client for local testing | MCP Inspector |

## Run Locally

Requires Python and Node.js (18 or newer for MCP Inspector).

1. Create and activate a virtual environment, then install the Python dependencies:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. Start the server:

   ```powershell
   python .\server.py
   ```

   The server listens on port `8080` by default. Set the `PORT` environment variable to use another port. The SSE MCP endpoint is `http://127.0.0.1:8080/sse`; the root URL `/` is not a web page and returns 404.

## Run with Docker

Requires Docker Engine or Docker Desktop. Before building the image, configure the server to listen on all container interfaces; otherwise, Docker port publishing cannot reach it. In `server.py`, use:

```python
mcp.run(transport="sse", host="0.0.0.0", port=port)
```

Build the image from the project directory:

```powershell
docker build -t demo-mcp-server .
```

Start the container and publish its port on localhost:

```powershell
docker run --rm --name demo-mcp-server -p 127.0.0.1:8080:8080 -e PORT=8080 demo-mcp-server
```

The server is then available to MCP clients at `http://127.0.0.1:8080/sse`. To stop it, press `Ctrl+C` in the terminal running the container. The `--rm` option removes the stopped container; omit it if you want to keep the container after stopping it.

## Test with MCP Inspector

In a second terminal, install the recorded npm dependencies and launch Inspector. If testing the locally running Python server, start it first using the instructions above. If testing the Docker container, leave that running and connect Inspector to the same endpoint:

```powershell
npm ci
npx @modelcontextprotocol/inspector
```

In Inspector, choose **SSE** transport and connect to `http://127.0.0.1:8080/sse`. Open the tools list, select a tool, and provide its inputs. For example:

```json
{
  "num1": 2,
  "num2": 3
}
```

The `add` result should be `5`. You can also try the other tools with:

```json
{
  "start": 1,
  "end": 7
}
```

This calls `randomizer` and returns a pseudorandom integer from 1 through 6.

```json
{
  "city": "Manila"
}
```

This calls `get_weather_info` and returns the response from wttr.in for Manila.
