# Image Validation

This example demonstrates how the generated image is validated against the original user requirements.

## User Request

```text
Create a picture of a cat.
```

## Validation Flow

```text
ImageGeneratorAgent
        ↓
Generated Image
        ↓
ImageValidatorAgent
        ↓
Validate Image Tool
        ↓
VALIDATION: PASS
        ↓
PASS
        ↓
END
```

## Validation Process

The `ImageValidatorAgent` receives two important pieces of information:

* The exact path of the generated image
* The original user requirements

These values are passed to the `validate_image` tool:

```text
image_path
requirements
```

The validation tool analyzes the generated image and compares it only against the explicitly provided requirements.

The validator checks requirements such as:

* Subject
* Objects
* Composition
* Colors
* Style
* Text
* Positioning
* Background
* Other explicitly requested details

The validator does not add additional requirements that were not specified by the user.

## Successful Validation

When the image satisfies the requirements, the validation tool returns:

```text
VALIDATION: PASS
```

The `ImageValidatorAgent` then returns:

```text
PASS
```

This triggers the team's termination condition.

## Purpose

This workflow separates image generation from image validation.

The generator is responsible for creating the image, while the validator independently evaluates whether the generated result satisfies the user's requirements.
