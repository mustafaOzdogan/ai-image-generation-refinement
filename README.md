# AI Image Generation & Iterative Refinement

A multi-agent image generation workflow built with **Microsoft AutoGen `SelectorGroupChat`**.

The system generates an image from a user requirement, validates the result against the original requirements, and automatically triggers a new generation cycle when validation fails.

> **Generate → Validate → Refine → Validate**

The goal is to demonstrate an **agentic feedback loop** rather than a simple image generation API call.

## Why This Project?

Image generation models can produce visually plausible results while still failing explicit user requirements.

For example:

> "Create a picture of a cat with exactly 3 ears."

An image generator may produce a cat with four ears.

Instead of accepting the first result, this project introduces a second agent that evaluates the generated image against the original requirements.

If validation fails, structured feedback is sent back to the generator and the image is regenerated.

This creates an iterative, feedback-driven workflow where validation is part of the execution loop rather than a final post-processing step.

## Key Features

* 🤖 Multi-agent image generation
* 🔍 Multimodal requirement validation
* 🔄 Automatic iterative refinement
* 🧠 Dynamic agent selection with `SelectorGroupChat`
* 🛠️ Tool-based image generation and validation
* 📋 Structured validation feedback
* 🛑 Configurable termination conditions
* 🎨 OpenAI image generation
* 🧩 AutoGen Studio workflow configuration


## Architecture

The workflow consists of two specialized agents coordinated by `SelectorGroupChat`.

```text
                    ┌─────────────────────────┐
                    │    User Requirement     │
                    └─────────────┬───────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │    SelectorGroupChat    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   ImageGeneratorAgent   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  Image Generation Tool  │
                    │     gpt-image-1-mini    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                           Generated Image
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   ImageValidatorAgent   │
                    └────────────┬────────────┘
                                 │
                         ┌───────┴───────┐
                         │               │
                       PASS            FAIL
                         │               │
                         ▼               ▼
                        END       Correction Feedback
                                         │
                                         ▼
                                  ImageGeneratorAgent
```

### Agent Responsibilities

| Component             | Responsibility                                                |
| --------------------- | ------------------------------------------------------------- |
| `ImageGeneratorAgent` | Generates images and applies correction feedback              |
| `ImageValidatorAgent` | Validates generated images against explicit user requirements |
| `SelectorGroupChat`   | Determines which agent should act next                        |
| Image Generation Tool | Generates images using `gpt-image-1-mini`                     |
| Image Validation Tool | Analyzes generated images and produces structured feedback    |

The agents have deliberately separated responsibilities:

* **Generator** focuses on creating and refining the image.
* **Validator** focuses on evaluating the result.
* **SelectorGroupChat** coordinates the workflow.

## How It Works

1. The user provides an image generation requirement.
2. `SelectorGroupChat` selects the `ImageGeneratorAgent`.
3. The generator creates an image using the image generation tool.
4. The generated image and original requirements are passed to the validator.
5. `ImageValidatorAgent` evaluates the image.
6. The validation tool returns either `PASS` or `FAIL`.
7. If validation passes, the workflow terminates.
8. If validation fails, the validator returns structured feedback.
9. `SelectorGroupChat` selects the generator again.
10. The generator uses the correction feedback while preserving requirements that were already satisfied.
11. The new image is validated again.

This cycle continues until the validation succeeds or the configured termination condition is reached.

---

## Example: Iterative Refinement

### User Requirement

```text
Create a picture of a cat with exactly 3 ears.
```
### First Generation

**Result:** Cat with 4 ears ❌

![First generation - cat with 4 ears](images/cat-4-ears.png)

### First Generation

```text
ImageGeneratorAgent
        ↓
Generated Image
        ↓
Cat with 4 ears
```

### Validation

```text
ImageValidatorAgent
        ↓
VALIDATION: FAIL
        ↓
OBSERVATION:
The cat has four ears instead of three.

CORRECTION:
Generate the cat with exactly three ears.
```

The correction is passed back to the generator.

### Refinement

```text
ImageGeneratorAgent
        ↓
New Image
        ↓
Cat with 3 ears
```

### Second Validation

```text
ImageValidatorAgent
        ↓
VALIDATION: PASS
        ↓
Workflow completed
```

The important part is that the first generated image is **not automatically accepted**.

The validator's feedback becomes input to the next generation cycle.

## Validation Contract

The validation tool uses a simple structured response format.

### Successful validation

```text
VALIDATION: PASS
```

The `ImageValidatorAgent` converts this to:

```text
PASS
```

which triggers the team's termination condition.

### Failed validation

```text
VALIDATION: FAIL
OBSERVATION: <what is wrong>
CORRECTION: <what should be changed>
```

The correction is passed back to the image generator through the agent conversation.

This provides a simple contract between the validation and generation stages.

## Technology Stack

| Component              | Technology          |
| ---------------------- | ------------------- |
| Agent Framework        | Microsoft AutoGen   |
| Orchestration          | `SelectorGroupChat` |
| Agent Reasoning        | `gpt-4o-mini`       |
| Image Generation       | `gpt-image-1-mini`  |
| Image Validation       | `gpt-4.1-mini`      |
| Language               | Python              |
| Workflow Configuration | AutoGen Studio      |

## Project Structure

```text
.
├── README.md
├── config/
│   └── selector_group_chat.json
├── tools/
│   ├── generate_image.py
│   └── validate_image.py
├── examples/
│   ├── basic_generation.md
│   ├── validation_pass.md
│   └── iterative_refinement.md
├── images/
│   └── .gitkeep
├── requirements.txt
├── .gitignore
└── .env.example
```

The `selector_group_chat.json` file contains the complete AutoGen `SelectorGroupChat` configuration exported from AutoGen Studio.

## Configuration

The main workflow is defined in:

```text
config/selector_group_chat.json
```

The configuration contains:

* `SelectorGroupChat`
* `ImageGeneratorAgent`
* `ImageValidatorAgent`
* Image generation tool
* Image validation tool
* Selector prompt
* Termination conditions

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Never commit your API key to GitHub.

A `.env.example` file is provided for configuration reference:

```env
OPENAI_API_KEY=
```

## Installation

Create a virtual environment and install the required dependencies.

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Workflow

The workflow can be imported into **AutoGen Studio** using the configuration file:

```text
config/selector_group_chat.json
```

After importing the team, provide an image generation request such as:

```text
Create a picture of a cat with exactly 3 ears.
```

The team should then execute the generation and validation loop automatically.

## Why SelectorGroupChat?

`SelectorGroupChat` dynamically determines which agent should act next based on the current workflow state.

The intended flow is:

```text
New Request
     ↓
ImageGeneratorAgent
     ↓
ImageValidatorAgent
     ↓
 ┌───┴────┐
PASS     FAIL
 │        │
 ▼        ▼
END   ImageGeneratorAgent
          ↓
      ImageValidatorAgent
          ↓
         ...
```

This makes the workflow suitable for iterative agent collaboration where the next action depends on the previous agent's output.

## Key Agentic AI Concepts

This project demonstrates:

* Multi-agent orchestration
* Agent role separation
* Tool calling
* Multimodal AI
* Image generation
* Image validation
* Structured tool output
* Feedback-driven refinement
* Dynamic agent selection
* Iterative agent workflows
* Termination conditions

The main architectural idea is to treat **validation as an active feedback mechanism**, rather than as a final passive check.

## Limitations

The validation process is model-based and therefore may not perfectly detect every visual discrepancy.

The current workflow also relies on the generated image being accessible through the file path provided by the image generation tool.

The number of refinement cycles is limited by the team's termination configuration.

## Future Improvements

Potential improvements include:

* Adding a maximum refinement/retry counter
* Supporting multiple generated candidates
* Comparing multiple images and selecting the best candidate
* Adding human approval before accepting the final image
* Persisting generation and validation history
* Adding image quality scoring
* Separating requirement validation from visual quality validation
* Adding additional specialized validators
* Supporting different image generation providers

## License

This project is licensed under the MIT License.
