# Relationship Calculator README

## Overview
The Relationship Calculator is a Python tool designed to calculate the type of relationship and comfort score between two users based on their typological aspects. It currently supports four typologies: Temporistics, Psychosophia, Amatoric, and Socionics.

## Features
- Determine relationship type based on user typologies.
- Provide a comfort score for the determined relationship type.
- Terminal color codes for visual comfort score representation.
- Support for multiple typologies.
  
## Relationship Types
The calculator can determine various relationship types, including but not limited to:
- Philia
- Pseudo-Philia
- Agape
- Full Agape
- Eros
- Eros Variant
- Full Eros

## Setup
1. Ensure that you have all the typology modules installed and imported.
2. Run the main function to start the program.

## Usage
Upon execution, the tool will:
1. Display a list of available typologies.
2. Ask the user to select desired typologies for compatibility calculation.
3. Prompt the user to choose types for both themselves and their partner based on the selected typologies.
4. Display the selected types and calculate the relationship type and comfort score.

## Extending Typologies
If you wish to add more typologies:
1. Import the new typology at the beginning of the script.
2. Add the new typology to the `available_typologies` dictionary.

## Notes
- The comfort score is determined based on predefined values for each relationship type.
- Terminal color codes are used to visually represent positive, neutral, or negative comfort scores.

## Contribution
Feel free to contribute to this project by adding new typologies, refining the relationship type determination logic, or enhancing the user interface.