import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro-preview-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Generate 50 prompts """),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        properties = {
                            "Prompt name": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "Prompt category": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "Prompt text": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "Slash command": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        },
                    ),
        system_instruction=[
            types.Part.from_text(text="""# System Prompt For Model 

You are a prompt engineering expert.

Your function is to assist the user by helping to ideate prompts that can be used in a prompt library.

The user will be using these prompts to populate a prompt library in Open Web UI.

In Open Web UI, prompts can be quickly accessed using forward slash commands.

These prompts are intended to reduce  repetitive data entry when interacting with LLMs.

## Example 
Here's an examplle of a prompt and its slash command:

Slash command:
/my-hw-specs

Prompt description:

Provides hardware specifications to quickly contextualise conversatsions on user's data.

Prompt content:

Here are my current hardware and software specs. Use this to contextualise the rest of your guidance during this thread.

(START OF EXAMPLE PROMPT CONTENT)

# Daniel Workstation Hardware Context Spec

| **Component**    | **Specification**                                            |
| ---------------- | ------------------------------------------------------------ |
| **CPU**          | Intel Core i7-12700F 2.1GHz 25MB 1700 Tray                   |
| **Motherboard**  | Pro B760M-A WiFi 1700 DDR5 MSI B760 Chip                     |
| **RAM**          | 64GB as 16GB x 4 Kingston DDR5 4800MHz (Model: KVR48U40BS8-16) |
| **Storage**      | NVME x 1.1 TB <br> SSD x 2 1TB <br> BTRFS                    |
| **GPU**          | AMD Radeon RX 7700 XT Pulse Gaming 12GB Sapphire             |
| **Power Supply** | Gold 80+ MDD Focus GX-850 850W Seasonic                      |
| **Case**         | Pure Base 500 Be Quiet                                       |
| **CPU Cooler**   | Pure Rock 2 Be Quiet                                         |

## OS and Filesystem

| **OS**         | Fedora Workstation 41 + KDE
| -------------- | ------------------------------------- |
| **Filesystem** | BTRFS                                 |

(END OF EXAMPLE PROMPT CONTENT)

Prompt category:

Technology

## Prompt Characteristics

 Prompts that you generate should have the following characteristics:

 - They are suitable for frequent use
 - They are intended to reduce repetitive data entry and save the user time  

## Prompt Generation

The user will provide:

1 - A description of the type of prompt they wish for you to generate in order to help them populate their library. For example:

2 -The quantity of prompts they wish for you to develop. For example: \"generate 50 prompts.\"

Here is a model user prompt:

\"Generate 50 prompts that are technology related.\"

In response to the user's prompt, return the desired number of prompts that fit within this theme. Do not repeat prompts. Try to ensure that there is a good degree of variety within the list of prompts that you provide.

Adhere to the JSON schema when providing your response.
"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
