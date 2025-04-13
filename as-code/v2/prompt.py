import base64
import os
import json
import csv
import re
from google import genai
from google.genai import types

# Read API key from .env file manually
def load_env_from_file():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key] = value

# Load environment variables
load_env_from_file()

def generate_filename(topic):
    """Generate a descriptive filename based on the topic."""
    # Convert to lowercase, replace spaces with hyphens, and remove special characters
    filename = re.sub(r'[^a-zA-Z0-9\s-]', '', topic.lower())
    filename = re.sub(r'\s+', '-', filename)
    return filename

def json_to_csv(json_file_path, csv_file_path):
    """Convert a JSON file to CSV format."""
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        if not data:
            print("Warning: No data found in " + json_file_path)
            return False
        
        # Get the field names from the first item
        field_names = data[0].keys()
        
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)
        
        print("Successfully converted " + json_file_path + " to " + csv_file_path)
        return True
    except Exception as e:
        print("Error converting JSON to CSV: " + str(e))
        return False

def ensure_directory_exists(directory):
    """Ensure that the specified directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Created directory: " + directory)

def generate(prompt_topic=None, prompt_count=50, output_file=None):
    """
    Generate prompts for a specific topic and save them to a file.
    
    Args:
        prompt_topic (str, optional): The topic for which to generate prompts. If None, user will be prompted.
        prompt_count (int, optional): The number of prompts to generate. Default is 50.
        output_file (str, optional): The file to save the prompts to. If None, a descriptive name will be generated.
    """
    # If no prompt topic is provided, ask the user
    if prompt_topic is None:
        prompt_topic = input("What type of prompts would you like to generate? (e.g., 'Python programming', 'Data science', 'Technology'): ")
    
    # If no prompt count is provided, ask the user
    if prompt_count is None:
        try:
            prompt_count = int(input("How many prompts would you like to generate? (default: 50): ") or "50")
        except ValueError:
            print("Invalid number, using default of 50.")
            prompt_count = 50
    
    # Generate descriptive filename if none provided
    if output_file is None:
        filename_base = generate_filename(prompt_topic)
        output_file = filename_base + "-prompts.json"
    
    # Ensure the created-prompts directory exists
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'created-prompts')
    ensure_directory_exists(output_dir)
    
    # Full path for the output files
    json_output_path = os.path.join(output_dir, output_file)
    csv_output_path = os.path.join(output_dir, output_file.replace('.json', '.csv'))
    
    print("\nGenerating " + str(prompt_count) + " prompts about '" + prompt_topic + "'...\n")
    
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="Generate " + str(prompt_count) + " prompts that are " + prompt_topic + " related."),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
                        type = genai.types.Type.ARRAY,
                        items = genai.types.Schema(
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
                    ),
        system_instruction=[
            types.Part.from_text(text="""# System Prompt For Model 

You are a prompt engineering expert.

Your function is to assist the user by helping to ideate prompts that can be used in a prompt library.

The user will be using these prompts to populate a prompt library in Open Web UI.

In Open Web UI, prompts can be quickly accessed using forward slash commands.

These prompts are intended to reduce  repetitive data entry when interacting with LLMs.

## Prompt Characteristics

 Prompts that you generate should have the following characteristics:

 - They are suitable for frequent use
 - They are intended to reduce repetitive data entry and save the user time  
 - All variables in the prompts should be enclosed in double curly brackets, like {{variable_name}}

## Prompt Generation

The user will provide:

1 - A description of the type of prompt they wish for you to generate in order to help them populate their library. For example:

2 -The quantity of prompts they wish for you to develop. For example: \"generate 50 prompts.\"

Here is a model user prompt:

\"Generate 50 prompts that are technology related.\"

In response to the user's prompt, return the desired number of prompts that fit within this theme. 

For every prompt, provide:

** Prompt name ** - Give the prompt a short name
** Prompt category ** - Assign a category for the prompt, like 'technology'. Try to minmimise the number of unique categories  you suggest on each run
** Prompt text ** - The text of the prompt. IMPORTANT: All variables in the prompt text should be enclosed in double curly brackets, like {{variable_name}} instead of [variable_name] or any other format.
** Slash command ** Your recommended slash command. Try to make this as short and easy to type as possible

Do not repeat prompts. Try to ensure that there is a good degree of variety within the list of prompts that you provide.

 

Adhere to the JSON schema when providing your response.


## Example For Modelling 

Here's an example of a prompt and its slash command:

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

## Variable Format Example

Example with variables using double curly brackets:

Prompt text: "Generate a {{language}} function that {{task_description}} with {{specific_requirements}}."

NOT like this: "Generate a [language] function that [task_description] with [specific_requirements]."

"""),
        ],
    )

    # Initialize an empty list to store all prompt data
    all_prompts = []
    full_response = ""

    print("Waiting for API response...")
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        chunk_text = chunk.text
        print(chunk_text, end="")
        full_response += chunk_text

    # Try to parse the full response as JSON
    try:
        # If the response is a single JSON object
        prompt_data = json.loads(full_response)
        if isinstance(prompt_data, list):
            all_prompts = prompt_data
        else:
            all_prompts.append(prompt_data)
    except json.JSONDecodeError:
        try:
            # Check if the response is a list of JSON objects
            if full_response.strip().startswith('[') and full_response.strip().endswith(']'):
                all_prompts = json.loads(full_response)
            else:
                # Try to parse each line as a separate JSON object
                lines = full_response.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and line != '[' and line != ']':
                        # Remove trailing commas if present
                        if line.endswith(','):
                            line = line[:-1]
                        try:
                            # Try to parse as JSON
                            if line.startswith('{') and line.endswith('}'):
                                prompt_data = json.loads(line)
                                all_prompts.append(prompt_data)
                        except json.JSONDecodeError:
                            continue
        except json.JSONDecodeError:
            print("\nWarning: Could not parse response as JSON. Saving raw text instead.")
            # Save the raw text if JSON parsing fails
            with open(json_output_path, 'w') as f:
                f.write(full_response)
            return json_output_path, None

    # Write the prompts to the JSON output file
    with open(json_output_path, 'w') as f:
        # Check if all_prompts is already a nested list
        if all_prompts and isinstance(all_prompts, list) and isinstance(all_prompts[0], list):
            # Flatten the nested list
            flattened_prompts = all_prompts[0]
            json.dump(flattened_prompts, f, indent=2)
        else:
            json.dump(all_prompts, f, indent=2)
    
    print("\nPrompts have been saved to " + json_output_path)
    
    # Convert JSON to CSV
    if json_to_csv(json_output_path, csv_output_path):
        print("CSV version saved to " + csv_output_path)
    
    return json_output_path, csv_output_path


def main():
    """Main function to run the prompt generator interactively."""
    print("=" * 50)
    print("Prompt Library Generator for Open Web UI")
    print("=" * 50)
    
    # Get the topic from the user
    prompt_topic = input("What type of prompts would you like to generate? (e.g., 'Python programming', 'Data science', 'Technology'): ")
    
    # Generate descriptive filename
    filename_base = generate_filename(prompt_topic)
    output_file = filename_base + "-prompts.json"
    
    # Get the count from the user
    try:
        prompt_count = int(input("How many prompts would you like to generate? (default: 50): ") or "50")
    except ValueError:
        print("Invalid number, using default of 50.")
        prompt_count = 50
    
    # Generate the prompts
    json_path, csv_path = generate(prompt_topic, prompt_count, output_file)
    
    # Ask if the user wants to view the generated prompts
    view_prompts = input("\nWould you like to view the generated prompts? (y/n): ").lower().strip() in ['y', 'yes']
    
    if view_prompts and json_path:
        try:
            with open(json_path, 'r') as f:
                prompts = json.load(f)
                
            print("\n" + "=" * 50)
            print("Generated " + str(len(prompts)) + " prompts about '" + prompt_topic + "':")
            print("=" * 50)
            
            for i, prompt in enumerate(prompts, 1):
                print("\n" + str(i) + ". " + prompt.get('Prompt name', 'Unnamed Prompt'))
                print("   Category: " + prompt.get('Prompt category', 'Uncategorized'))
                print("   Command: " + prompt.get('Slash command', 'No command'))
                print("   Text: " + prompt.get('Prompt text', 'No text')[:100] + "...")
        except Exception as e:
            print("Error viewing prompts: " + str(e))


if __name__ == "__main__":
    main()
