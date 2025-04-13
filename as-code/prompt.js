const {
    GoogleGenerativeAI,
    HarmCategory,
    HarmBlockThreshold,
  } = require("@google/generative-ai");
  const fs = require("node:fs");
  const mime = require("mime-types");
  
  const apiKey = process.env.GEMINI_API_KEY;
  const genAI = new GoogleGenerativeAI(apiKey);
  
  const model = genAI.getGenerativeModel({
    model: "gemini-2.5-pro-preview-03-25",
    systemInstruction: "# System Prompt For Model \n\nYou are a prompt engineering expert.\n\nYour function is to assist the user by helping to ideate prompts that can be used in a prompt library.\n\nThe user will be using these prompts to populate a prompt library in Open Web UI.\n\nIn Open Web UI, prompts can be quickly accessed using forward slash commands.\n\nThese prompts are intended to reduce  repetitive data entry when interacting with LLMs.\n\n## Example \nHere's an examplle of a prompt and its slash command:\n\nSlash command:\n/my-hw-specs\n\nPrompt description:\n\nProvides hardware specifications to quickly contextualise conversatsions on user's data.\n\nPrompt content:\n\nHere are my current hardware and software specs. Use this to contextualise the rest of your guidance during this thread.\n\n(START OF EXAMPLE PROMPT CONTENT)\n\n# Daniel Workstation Hardware Context Spec\n\n| **Component**    | **Specification**                                            |\n| ---------------- | ------------------------------------------------------------ |\n| **CPU**          | Intel Core i7-12700F 2.1GHz 25MB 1700 Tray                   |\n| **Motherboard**  | Pro B760M-A WiFi 1700 DDR5 MSI B760 Chip                     |\n| **RAM**          | 64GB as 16GB x 4 Kingston DDR5 4800MHz (Model: KVR48U40BS8-16) |\n| **Storage**      | NVME x 1.1 TB <br> SSD x 2 1TB <br> BTRFS                    |\n| **GPU**          | AMD Radeon RX 7700 XT Pulse Gaming 12GB Sapphire             |\n| **Power Supply** | Gold 80+ MDD Focus GX-850 850W Seasonic                      |\n| **Case**         | Pure Base 500 Be Quiet                                       |\n| **CPU Cooler**   | Pure Rock 2 Be Quiet                                         |\n\n## OS and Filesystem\n\n| **OS**         | Fedora Workstation 41 + KDE\n| -------------- | ------------------------------------- |\n| **Filesystem** | BTRFS                                 |\n\n(END OF EXAMPLE PROMPT CONTENT)\n\nPrompt category:\n\nTechnology\n\n## Prompt Characteristics\n\n Prompts that you generate should have the following characteristics:\n\n - They are suitable for frequent use\n - They are intended to reduce repetitive data entry and save the user time  \n\n## Prompt Generation\n\nThe user will provide:\n\n1 - A description of the type of prompt they wish for you to generate in order to help them populate their library. For example:\n\n2 -The quantity of prompts they wish for you to develop. For example: \"generate 50 prompts.\"\n\nHere is a model user prompt:\n\n\"Generate 50 prompts that are technology related.\"\n\nIn response to the user's prompt, return the desired number of prompts that fit within this theme. Do not repeat prompts. Try to ensure that there is a good degree of variety within the list of prompts that you provide.\n\nAdhere to the JSON schema when providing your response.\n",
  });
  
  const generationConfig = {
    temperature: 1,
    topP: 0.95,
    topK: 64,
    maxOutputTokens: 65536,
    responseModalities: [
    ],
    responseMimeType: "application/json",
    responseSchema: {
      type: "object",
      properties: {
        "Prompt name": {
          type: "string"
        },
        "Prompt category": {
          type: "string"
        },
        "Prompt text": {
          type: "string"
        },
        "Slash command": {
          type: "string"
        }
      }
    },
  };
  
  async function run() {
    const chatSession = model.startChat({
      generationConfig,
      history: [
      ],
    });
  
    const result = await chatSession.sendMessage("Generate 50 prompts ");
    // TODO: Following code needs to be updated for client-side apps.
    const candidates = result.response.candidates;
    for(let candidate_index = 0; candidate_index < candidates.length; candidate_index++) {
      for(let part_index = 0; part_index < candidates[candidate_index].content.parts.length; part_index++) {
        const part = candidates[candidate_index].content.parts[part_index];
        if(part.inlineData) {
          try {
            const filename = `output_${candidate_index}_${part_index}.${mime.extension(part.inlineData.mimeType)}`;
            fs.writeFileSync(filename, Buffer.from(part.inlineData.data, 'base64'));
            console.log(`Output written to: ${filename}`);
          } catch (err) {
            console.error(err);
          }
        }
      }
    }
    console.log(result.response.text());
  }
  
  run();