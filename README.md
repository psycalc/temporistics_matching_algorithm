Sure, here's the full `README.md` with the updated "Supported Relationship Types" section:

```markdown
# Relationship Calculator

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Supported Relationship Types](#supported-relationship-types)
  - [Temporistics](#temporistics)
  - [Psychosophia](#psychosophia)
  - [Amatoric](#amatoric)
  - [Socionics](#socionics)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Extending Typologies](#extending-typologies)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)
- [Screenshots](#screenshots)
- [Video Demonstration](#video-demonstration)

## Overview

The Relationship Calculator is an innovative Python application that evaluates compatibility between individuals based on psychological typologies. It currently supports Temporistics, Psychosophia, Amatoric, and Socionics, providing a unique perspective on interpersonal dynamics.

## Features

- Assess relationship types across various typologies.
- Calculate and display comfort scores for relationships.
- Visual representation of comfort scores with terminal color codes.
- Extensible architecture to incorporate more typologies.

## Supported Relationship Types

The tool evaluates multiple relationship dynamics across the following typologies:

### Temporistics

Temporistics is a psychological typology that categorizes people based on their relationship with time and temporal perspectives. It focuses on how individuals perceive and interact with the past, present, future, and eternity.

### Psychosophia

Psychosophia, also known as the Philosophical Typology, is a system that classifies individuals based on their core psychological aspects: Emotion, Logic, Will, and Power. It explores the interplay between these aspects and their influence on behavior and decision-making.

### Amatoric

The Amatoric Typology is centered around the concepts of love, passion, friendship, and romance. It aims to understand and categorize individuals based on their attitudes, values, and approaches to interpersonal relationships and emotional connections.

### Socionics

Socionics is a pseudoscientific theory that describes personality types based on a combination of different psychological traits, such as introversion/extraversion, logic/ethics, intuition/sensing, and rationality/irrationality. It provides insights into interpersonal dynamics and compatibility between types.

The tool evaluates relationship types like Philia, Eros, Dual, Conflict, and Mirror across these typologies, providing a unique perspective on interpersonal dynamics and compatibility.

## Prerequisites

Ensure you have the following:

- Python 3.8+
- Pip (Python package installer)

## Installation

To set up the project locally:

1. Clone the repository:

```bash
git clone https://github.com/your-username/relationship-calculator.git
```

2. Navigate to the project directory:

```bash
cd relationship-calculator
```

3. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Set the required environment variables:

```bash
export FLASK_CONFIG=development  # or 'production', 'testing'
export SECRET_KEY=your-secret-key
# Set other environment variables as needed
```

2. Start the application:

```bash
python run.py
```

3. Navigate to `http://localhost:5000` to use the tool.

## Extending Typologies

To add a new typology:

1. Create a new class in `app/typologies`.
2. Update the `available_typologies` dictionary in the calculation module.

## Contributing

We welcome contributions! Here's how to help:

1. Fork the repository.
2. Create your feature branch: `git checkout -b new-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin new-feature`.
5. Submit a pull request.

Consult [GitHub documentation](https://help.github.com/articles/creating-a-pull-request/) for more on pull requests.

## Troubleshooting

If you encounter issues:

- Check Python and Pip versions.
- Ensure all environment variables are set correctly.
- Look at the error logs for specifics and adjust accordingly.
- Common issues and their solutions:
  - **Issue 1**: Description and resolution steps.
  - **Issue 2**: Description and resolution steps.
  - ...

## License

This project is under the [MIT License](LICENSE).

## Acknowledgements

- Inspired by diverse psychological typologies.
- Thanks to contributors for enhancements and feedback.

## Contact

For questions or feedback, email us at `your.email@example.com`.

## Screenshots

(Include a few screenshots of your application here to make the README visually appealing)

## Video Demonstration

(Optionally, include a link to a short video demo of the application)

Remember to replace placeholders like `your-username` and `your.email@example.com` with your actual information.
```