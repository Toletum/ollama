import datetime
import sys
from zoneinfo import ZoneInfo
import uuid

import geocoder
import ollama
import requests
from pydantic import json


def get_time(timezone: str) -> str:
    """Returns the current time in ISO 8601 format."""
    try:
        zona = ZoneInfo(timezone)
        now = datetime.datetime.now(zona)
    except Exception as ex:
        now = datetime.datetime.utcnow()
    return f"Current time: {now.strftime('%H:%M:%S')} {timezone}"


def get_coor(city: str) -> json:
    """Return in json forma the coordinates for the city."""

    session = requests.Session()
    session.proxies.update({
        "http": "http://de1app02903n-2.internal.vodafone.com:8080",
        "https": "http://de1app02903n-2.internal.vodafone.com:8080",
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



AVAILABLE_FUNCTIONS = {
    'get_time': get_time,
    'get_coor': get_coor
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Returns the current UTC time in ISO 8601 format.",
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


messages = [
    {
        'role': 'user',
        'content': "what time is it now in Bilbao localtime and UTC time too and coordinates?",
    } ]


modulo_actual = sys.modules[__name__]

while True:
    response = ollama.chat(
        model="llama3.1:latest",
        messages=messages,
        tools=TOOLS
    )

    messages.append(response['message'])

    if len(response['message'].get('tool_calls', [])) == 0:
        print(response['message'])
        break


    for tool_call in response['message']['tool_calls']:
        function_name = tool_call['function']['name']
        function_args = tool_call['function']['arguments']
        try:
            function_call = getattr(modulo_actual, function_name)
            function_response = function_call(**function_args)
            messages.append({
                "role": "tool",
                "content": str(function_response),
                "tool_call_id": str(uuid.uuid4())
            })
            print(f"tool: '{function_name}' args: {function_args} -> {str(function_response)}")
        except Exception as ex:
            print(f"ERROR tool: '{function_name}' args: {function_args}")
            pass
