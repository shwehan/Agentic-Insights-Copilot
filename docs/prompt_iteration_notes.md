# Prompt Iteration Notes

## Version 1
Issue:
- invented target population details
- too confident when context was broad

## Version 2
Change:
- told model to use only retrieved context
- told model to say when information is unspecified
- told model not to invent population definitions

Result:
- more grounded
- less polished maybe, but more reliable

## Iteration 1 findings
- model invents target population scope and time windows
- model overuses rewards-specific variables for broader prompts
- outputs are readable and well-structured
- next step: tighten grounding prompt and add missing_information field

## Iteration 2 findings
- reduced unsupported assumptions
- added alternative approaches and missing information
- output feels more like a planning assistant than a fully certain analyst