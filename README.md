# Multi-Agent Image Generation & Validation

A multi-agent image generation workflow built with **Microsoft AutoGen `SelectorGroupChat`**.

The system generates images from user requirements, validates the generated image against those requirements, and automatically triggers an iterative refinement cycle when validation fails.

## Overview

This project demonstrates how multiple AI agents can collaborate in an image generation workflow.

The system consists of:

* **ImageGeneratorAgent** — generates images and applies correction feedback.
* **ImageValidatorAgent** — validates generated images against the original user requirements.
* **SelectorGroupChat** — determines which agent should act next.
* **Image Generation Tool** — generates images using OpenAI's `gpt-image-1-mini`.
* **Validation Tool** — analyzes the generated image and returns structured validation feedback.

The main goal is to demonstrate an **agentic feedback loop** rather than a simple image generation API call.

---

## Architecture

```text
                         ┌─────────────────┐
                         │      User       │
                         └────────┬────────┘
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
                    │     gpt-image-1-mini     │
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
                                         │
                                         └──────► Generator
```

---

## How It Works

The workflow follows these steps:

1. The user provides an image generation request.
2. `SelectorGroupChat` selects the `ImageGeneratorAgent`.
3. `ImageGeneratorAgent` generates an image using the image generation tool.
4. The agent reports:

   * The original requirements
   * The generated image path
5. `SelectorGroupChat` selects the `ImageValidatorAgent`.
6. `ImageValidatorAgent` sends the generated image and the original requirements to the validation tool.
7. The validation tool returns either:

   * `VALIDATION: PASS`
   * `VALIDATION: FAIL`
8. If validation passes, the workflow terminates.
9. If validation fails, the validator provides:

   * `OBSERVATION`
   * `CORRECTION`
10. `SelectorGroupChat` selects the `ImageGeneratorAgent` again.
11. The generator creates a new image while preserving the requirements that were already satisfied.
12. The new image is validated again.

This creates an iterative generation → validation → refinement loop.

---

## Use Cases

### 1. Basic Image Generation

A simple request can be handled by the workflow:

```text
User:
Create a picture of a cat.
```

The generator creates the image and the validator checks whether the generated image satisfies the request.

If the requirements are satisfied:

```text
VALIDATION: PASS
```

The validator agent returns:

```text
PASS
```

and the workflow terminates.

---

### 2. Requirement-Based Image Validation

The validator does not simply check whether an image exists.

It evaluates the generated image against the **explicit requirements provided by the user**.

For example:

```text
User:
Create a picture of a cat with exactly 3 ears.
```

The generator may initially produce an incorrect image:

```text
Generated Image:
Cat with 4 ears
```

The validator can return:

```text
VALIDATION: FAIL
OBSERVATION: The cat has four ears instead of three.
CORRECTION: Generate the cat with exactly three ears.
```

The validation result is then used as feedback for the next generation cycle.

---

### 3. Iterative Image Refinement

This is the primary use case demonstrated by the project.

Example workflow:

```text
User:
Create a picture of a cat with exactly 3 ears.
```

First generation:

```text
ImageGeneratorAgent
        ↓
Generated Image
        ↓
Cat with 4 ears
```

Validation:

```text
ImageValidatorAgent
        ↓
VALIDATION: FAIL
        ↓
Correction:
"Generate the cat with exactly three ears."
```

The `SelectorGroupChat` then selects the generator again:

```text
ImageGeneratorAgent
        ↓
New Image
        ↓
Cat with 3 ears
```

Second validation:

```text
ImageValidatorAgent
        ↓
VALIDATION: PASS
        ↓
PASS
        ↓
Workflow completed
```

This demonstrates that the system can use validation feedback to trigger another generation cycle instead of simply accepting the first generated result.

---

## Agent Responsibilities

| Component               | Responsibility                                                |
| ----------------------- | ------------------------------------------------------------- |
| `ImageGeneratorAgent`   | Generates images and applies correction feedback              |
| `ImageValidatorAgent`   | Validates generated images against explicit user requirements |
| `SelectorGroupChat`     | Selects the next agent based on the current workflow state    |
| `Image Generation Tool` | Generates images using `gpt-image-1-mini`                     |
| `Validate Image Tool`   | Evaluates generated images and produces structured feedback   |

---

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

---

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
└── .env.example
```

The `selector_group_chat.json` file contains the complete AutoGen `SelectorGroupChat` configuration exported from AutoGen Studio.

---

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

The team uses `gpt-4o-mini` for agent reasoning and `gpt-image-1-mini` for image generation.

The validation tool currently uses `gpt-4.1-mini` for image analysis.

---

## Environment Variables

Create a `.env` file or configure the environment variable:

```text
OPENAI_API_KEY=your_api_key_here
```

Do not commit your API key to GitHub.

A `.env.example` file can be included as:

```text
OPENAI_API_KEY=
```

---

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

---

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

---

## Why SelectorGroupChat?

`SelectorGroupChat` is used to dynamically determine which agent should act next.

The selector follows the workflow rules:

```text
New request
    ↓
ImageGeneratorAgent
    ↓
ImageValidatorAgent
    ↓
PASS → End
    │
    └── FAIL → ImageGeneratorAgent
                    ↓
               ImageValidatorAgent
```

This allows the workflow to continue iterating only when the validation result requires another generation.

---

## Key Concepts Demonstrated

This project demonstrates several concepts relevant to agentic AI systems:

* Multi-agent orchestration
* Agent role separation
* Tool calling
* Image generation
* Multimodal image validation
* Structured tool output
* Feedback-driven refinement
* Dynamic agent selection
* Termination conditions
* Iterative agent workflows

---

## Limitations

The validation process is model-based and therefore may not perfectly detect every visual discrepancy.

The current workflow also relies on the generated image being accessible through the file path provided by the image generation tool.

The number of refinement cycles is limited by the team's termination configuration.

---

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

---

## Example Workflow

```text
                    User Request
                         │
                         ▼
                SelectorGroupChat
                         │
                         ▼
              ImageGeneratorAgent
                         │
                         ▼
               Image Generation
                         │
                         ▼
                 Generated PNG
                         │
                         ▼
              ImageValidatorAgent
                         │
                ┌────────┴────────┐
                │                 │
               PASS              FAIL
                │                 │
                ▼                 ▼
              Finish        Correction Feedback
                                  │
                                  ▼
                         ImageGeneratorAgent
                                  │
                                  ▼
                           New Generation
                                  │
                                  ▼
                         ImageValidatorAgent
                                  │
                            ┌─────┴─────┐
                            │           │
                           PASS        FAIL
                            │           │
                            ▼           └──► Iterate
                          Finish
```

---

## License

Add your preferred license here.
