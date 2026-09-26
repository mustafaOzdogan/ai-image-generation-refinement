# Iterative Image Refinement

This example demonstrates the complete feedback loop of the multi-agent workflow.

The system detects an incorrect initial generation, generates correction feedback, and automatically triggers another generation cycle.

## User Request

```text
Create a picture of a cat with exactly 3 ears.
```

## Initial Generation

The `SelectorGroupChat` selects the `ImageGeneratorAgent`.

```text
User Request
     ↓
ImageGeneratorAgent
     ↓
Image Generation Tool
     ↓
Generated Image
```

The first generated image contains a cat with four ears.

```text
Generated Result:
Cat with 4 ears
```

## Validation

The `ImageValidatorAgent` receives:

```text
IMAGE_PATH: <generated image path>

REQUIREMENTS: Create a picture of a cat with exactly 3 ears.
```

The validation tool compares the generated image against the original requirements.

The tool returns:

```text
VALIDATION: FAIL
OBSERVATION: The cat has four ears instead of three.
CORRECTION: Generate the cat with exactly three ears.
```

## Refinement

The `SelectorGroupChat` detects the failed validation and selects the `ImageGeneratorAgent` again.

```text
ImageValidatorAgent
        ↓
VALIDATION: FAIL
        ↓
Correction Feedback
        ↓
SelectorGroupChat
        ↓
ImageGeneratorAgent
```

The generator uses the correction feedback while preserving the original user requirements.

A new image is generated:

```text
New Generated Result:
Cat with 3 ears
```

## Final Validation

The new image is passed to the `ImageValidatorAgent`.

The validation tool returns:

```text
VALIDATION: PASS
```

The validator agent converts this to:

```text
PASS
```

The `TextMentionTermination` condition detects `PASS` and terminates the workflow.

## Complete Workflow

```text
                     User Request
                          ↓
                 ImageGeneratorAgent
                          ↓
                   Generated Image
                          ↓
                 ImageValidatorAgent
                          ↓
                       FAIL
                          ↓
                 Correction Feedback
                          ↓
                 SelectorGroupChat
                          ↓
                 ImageGeneratorAgent
                          ↓
                    New Image
                          ↓
                 ImageValidatorAgent
                          ↓
                       PASS
                          ↓
                        END
```

## What This Demonstrates

This example demonstrates the main agentic behavior of the project:

* Multi-agent collaboration
* Dynamic agent selection
* Image generation
* Multimodal image validation
* Structured validation feedback
* Feedback-driven image refinement
* Iterative generation
* Automatic workflow termination

The important part is that the second generation is not triggered manually. The failed validation result causes `SelectorGroupChat` to select the generator again, creating an automated refinement loop.
