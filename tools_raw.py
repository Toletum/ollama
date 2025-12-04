import datetime
import sys
import os
import time
from zoneinfo import ZoneInfo
import uuid


from functools import lru_cache

import geocoder
import ollama
import requests
from pydantic import json

"""
Using tools in ollama from the scratch, no framework

TOOLS:
    get_time: Returns the current time in ISO 8601 format
    get_coor: Return in json forma the coordinates for the city

The tools are cached because sometime the call is repeat


"""



@lru_cache(maxsize=1024)
def get_time(timezone: str) -> json:
    """Returns the current time in ISO 8601 format."""
    try:
        tz = ZoneInfo(timezone)
        now = datetime.datetime.now(tz)
    except Exception as ex:
        now = datetime.datetime.now(datetime.timezone.utc)
    return {
        'timezone': timezone,
        'tz': repr(tz),
        'time': now.strftime('%H:%M:%S')
    }
# ----------------------------------------------------------------------------------

@lru_cache(maxsize=1024)
def get_coor(city: str) -> json:
    """Return in json forma the coordinates for the city."""

    session = requests.Session()
    session.proxies.update({
        "http": os.getenv("PROXY", None),
        "https": os.getenv("PROXY", None),
    })

    session.headers.update({
    'User-Agent': 'MyGeocodingScript/1.0 (contact@mycompany.com)'
    })

    try:
        g = geocoder.osm(location=city, session=session, timeout=10.0)

        return {
            "city": city,
            "latitude": g.lat,
            "longitude": g.lng
        }
    except Exception as ex:
        return {
            "city": city,
            "error": repr(ex)
        }
# ----------------------------------------------------------------------------------

# Doc tools
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Return in json format current time in ISO 8601 format.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA timezone string, e.g., 'UTC', 'Europe/Madrid', 'America/New_York'."
                    }
                },
                "required": ["timezone"]
            }
        }
    },
    {
    "type": "function",
        "function": {
            "name": "get_coor",
            "description": "Return in json format the coordinates for the city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city, p.ej. 'Madrid', 'Barcelona'."
                    }
                },
                "required": ["city"]
            }
        }
    }
]

#  Initial message: The request
messages = [
    {
        'role': 'user',
        'content': """what time is it now in Bilbao localtime, UTC time and latitude/longitude?
            Be brief, one or two lines at most.
        """,
    } ]

#  NO TOOLS
print("---- NO TOOLS ----")
response = ollama.chat(
    model="llama3.1:latest",
    messages=messages
)

print("---- RESPONSE ----")
print(response['message']['content'])
print("---- NO TOOLS ----")


module = sys.modules[__name__]

print("---- TOOLS ----")

loop = 0
while True: #  Until no tools to call
    loop += 1
    print(f"Loop {loop}")
    response = ollama.chat(
        model="llama3.1:latest",
        messages=messages,
        tools=TOOLS #  Register tools
    )

    # History
    messages.append(response['message'])

    if len(response['message'].get('tool_calls', [])) == 0: #  No more tools to call
        break #  Bye bye

    for tool_call in response['message']['tool_calls']:
        function_name = tool_call['function']['name']
        function_args = tool_call['function']['arguments']
        try:
            calling = time.time()
            print(f"Calling... '{function_name}' args: {function_args}")
            function_call = getattr(module, function_name)
            response = function_call(**function_args)
            # Add to the context
            messages.append({
                "role": "tool",
                "content": str(response),
                "tool_call_id": str(uuid.uuid4())
            })
            round(time.time() - calling, 4)
            print(f"    REQUEST: {round(time.time() - calling, 4)}  DATA: {str(response)}")
        except Exception as ex:
            print(f"ERROR tool: '{function_name}' args: {function_args}")
            pass


# The final response
print("---- RESPONSE ----")
print(response['message']['content'])
print("---- TOOLS ----")
