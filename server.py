import logging
import os
import sys

# test: for random words
import random

# test: for API calls
import requests

# for MCP server
from mcp.server.mcpserver import MCPServer

name = "demo-mcp-server"
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(name)
port = int(os.environ.get('PORT', 8080))
mcp = MCPServer(name, log_level="INFO")

# test: add
@mcp.tool()
def add(num1: int, num2: int) -> int:
    """Adds two numbers.

    Args:
        num1 (int): The augend of the operation.
        num2 (int): The addend of the operation.

    Returns:
        int: The sum of the operation.
    """
    
    logger.info(f"Tool called: add({num1}, {num2})")
    return num1 + num2

# test: random number
@mcp.tool()
def randomizer(start: int, end: int) -> int:
    """Picks a random number from a given range.

    Args:
        start (int): The starting number of the range.
        end (int): The ending number of the range.

    Returns:
        int: A pseudorandom chosen number within the given range.
    """

    logger.info(f"Tool called: randomizer({start}, {end})")
    return random.randrange(start, end)

# test: weather
@mcp.tool()
def get_weather_info(city: str) -> str:
    """Gets current weather for a given city.

    Args:
        city (str): A city that exists on Earth.

    Returns:
        str: The weather information from the given city.
    """

    logger.info(f"Tool called: get_weather_info({city})")
    try:
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}", timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        request_error = f"Error fetching weather info: {str(e)}"
        logger.error(request_error)
        return request_error

if __name__ == "__main__":
    logger.info(f"Running MCP server on port {port}.")
    try:
        mcp.run(transport="sse", port=port)
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("MCP server terminated.")
