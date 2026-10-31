from google.adk import Agent


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city: The name of the city (e.g. 'New York', 'London', 'Tokyo').
    """
    # Replace with real logic or external API call as needed
    return {
        "status": "success",
        "city": city,
        "time": "12:00 PM",
    }


# Root agent configured for Vertex AI
# ADK automatically picks up GOOGLE_GENAI_USE_VERTEXAI, GOOGLE_CLOUD_PROJECT,
# and GOOGLE_CLOUD_LOCATION from your .env file or environment variables.
root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="vertex_agent",
    description="Assistant powered by Gemini on Vertex AI.",
    instruction=(
        "You are a helpful assistant powered by Google Cloud Vertex AI. "
        "Use available tools when necessary to assist the user."
    ),
    tools=[get_current_time],
)
