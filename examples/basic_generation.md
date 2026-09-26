# Basic Image Generation

This example demonstrates the basic image generation workflow using the `ImageGeneratorAgent`.

## User Request

```text
Create a picture of a cat.
```

## Workflow

```text
User
  ↓
SelectorGroupChat
  ↓
ImageGeneratorAgent
  ↓
Image Generation Tool
  ↓
Generated Image
  ↓
ImageValidatorAgent
  ↓
PASS
  ↓
END
```

## Process

1. The user provides an image generation request.
2. `SelectorGroupChat` selects the `ImageGeneratorAgent`.
3. `ImageGeneratorAgent` generates the image using the image generation tool.
4. The generated image path and original requirements are provided to the `ImageValidatorAgent`.
5. `ImageValidatorAgent` validates the image against the original requirements.
6. If the requirements are satisfied, the validator returns:

```text
VALIDATION: PASS
```

7. The validator agent returns:

```text
PASS
```

8. The `TextMentionTermination` condition detects `PASS` and terminates the workflow.

## Expected Result

A generated image of a cat is produced and validated successfully.

This example demonstrates the basic generation and validation path without requiring an iterative refinement cycle.
