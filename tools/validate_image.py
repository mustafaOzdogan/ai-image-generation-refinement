import base64
import os
from openai import OpenAI


def validate_image(image_path: str,  requirements: str) -> str:
    """
    Validates a generated image against the original user requirements.

    Args:
        image_path: Path of the generated image.
        requirements: Original user requirements for the image.

    Returns:
        PASS if the image satisfies the requirements,
        otherwise FAIL with an explanation.
    """

    api_key = os.environ['OPENAI_API_KEY']

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable could not be found."
        )

    client = OpenAI(api_key=api_key)

    # Function to encode the image 
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    # Getting the base64 string
    base64_image = encode_image(image_path)

    validation_prompt = f"""
                        Inspect this generated image and compare it against
                        the original user requirements.

                        ORIGINAL USER REQUIREMENTS:
                        {requirements}

                        Check the generated image against
                        ONLY the requirements explicitly stated above.

                        Check:
                        - Subject
                        - Composition
                        - Objects
                        - Colors
                        - Style
                        - Text
                        - Positioning
                        - Background
                        - Other explicitly requested details

                        Do not invent additional requirements.

                        Return exactly one of these formats:

                        VALIDATION: PASS

                        or

                        VALIDATION: FAIL
                        OBSERVATION: <what is wrong in the generated image>
                        CORRECTION: <exactly what the generator should change>
                        """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": validation_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content
