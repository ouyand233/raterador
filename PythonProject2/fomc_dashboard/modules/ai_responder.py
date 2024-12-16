from openai import AzureOpenAI


class AzureOpenAIHelper:
    """
    Helper class for interacting with the Azure OpenAI service.
    Designed to simplify API calls and integrate functionality.
    """

    AZURE_ENDPOINT = "https://hkust.azure-api.net"  # Replace with your endpoint
    API_VERSION = "2024-06-01"  # API version
    DEFAULT_MODEL = "gpt-4o-mini"  # Default model to use

    def __init__(self, api_key):
        """
        Initialize the AzureOpenAIHelper instance.

        Args:
            api_key (str): Your Azure OpenAI API key.
        """
        self.client = AzureOpenAI(
            azure_endpoint=self.AZURE_ENDPOINT,
            api_version=self.API_VERSION,
            api_key=api_key
        )

    def get_response(self, message, instruction, model=None, temperature=1.0):
        """
        Send a chat completion request to Azure OpenAI.

        Args:
            message (str): User's input message.
            instruction (str): System's role or guiding instruction.
            model (str, optional): Model to use. Defaults to DEFAULT_MODEL.
            temperature (float, optional): Sampling temperature. Defaults to 1.0.

        Returns:
            str: AI-generated response.
        """
        model = model or self.DEFAULT_MODEL

        try:
            response = self.client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": message}
                ]
            )
            # Print token usage
            print(f"Token Usage: {response.usage}")
            # Return the response content
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error during API call: {e}")
            return None


# Example usage
if __name__ == "__main__":
    PRIMARY_KEY = "198ee87d93034da5a0a72a684483c44e"  # Replace with your actual key

    # Initialize the helper
    ai_helper = AzureOpenAIHelper(api_key=PRIMARY_KEY)

    # FOMC-specific instruction
    instruction = (
        "You are an assistant providing real-time updates on FOMC meetings. "
        "Summarize key discussions, decisions, and macroeconomic implications."
    )

    # Get a response for a specific question
    response = ai_helper.get_response(
        message="What are the latest insights from the FOMC meeting?",
        instruction=instruction
    )

    # Print the AI's response
    if response:
        print(f"AI Response: {response}")
