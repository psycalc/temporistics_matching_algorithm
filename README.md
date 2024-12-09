# Psychological Calculator Project

**Table of Contents:**
1. [Project Description](#project-description)
2. [Theoretical Foundations](#theoretical-foundations)
    - [Temporistics (Time)](#temporistics-time)
    - [Psychosophy (Personality Aspects)](#psychosophy-personality-aspects)
    - [Socionics (Modeling of Information)](#socionics-modeling-of-information)
3. [Implementation in Code](#implementation-in-code)
    - [Typology Classes](#typology-classes)
    - [Services and Data Validation](#services-and-data-validation)
    - [Routes and Forms](#routes-and-forms)
4. [Testing](#testing)
5. [Installation and Run](#installation-and-run)
6. [Additional Information](#additional-information)

---

## Project Description

This project integrates theoretical concepts from three typologies (Temporistics, Psychosophy, and Socionics) and implements them in a web application. Users can select their types, calculate relationships between types, and view the "comfort score" of these interactions.

The main goal is to demonstrate how theoretical models of perception (time, personality aspects, information) can be transformed into practical code, tested thoroughly, and presented through a web interface.

## Theoretical Foundations

### Temporistics (Time)
- **Four aspects:** Past, Current, Future, Eternity.
- **Induction vs. Deduction:**
  - Positions 1 & 4: Deductive (acting based on a preformed overall picture of time).
  - Positions 2 & 3: Inductive (collecting and analyzing information about time).

Conflict arises when one person operates deductively from a big-picture principle, while another uses induction, gathering data and adapting continuously.

### Psychosophy (Personality Aspects)
- **Four aspects:** Emotion, Logic, Will, Physics.
- **Analysis vs. Synthesis:**
  - Positions 1 & 4: Synthetic (holistic perception of the aspect).
  - Positions 2 & 3: Analytic (breaking the aspect down into components).

Conflict: a synthetic individual acts holistically without dissecting details, while an analytic individual seeks to break everything down and understand each part.

### Socionics (Modeling of Information)
- Focuses on logical, ethical, sensory, and intuitive modeling of information.
- Each type perceives and processes information differently:
  - The logician uses systems and structures,
  - The ethicist focuses on emotional exchange,
  - The sensor relies on tangible, concrete reality,
  - The intuit deals with abstract concepts and possibilities.

Conflict: Different types struggle to "mirror" or understand the other's model of perception.

## Implementation in Code

### Typology Classes
Under `app/typologies/`, each typology is implemented as a class derived from an abstract `Typology`. They provide methods like:
- `get_all_types()` to retrieve all types.
- `shorten_type()` to abbreviate type names.
- `determine_relationship_type()` to calculate the relationship type between two given types.
- `get_comfort_score()` to determine a "comfort score" based on their relationship.

These methods directly reflect the theoretical principles: induction/deduction (Temporistics), analysis/synthesis (Psychosophy), and modeling (Socionics).

### Services and Data Validation
`services.py` contains:
- `get_types_by_typology()`: returns type lists according to the chosen typology class.
- `calculate_relationship(user1, user2, typology)`: applies typology logic to determine relationship type and comfort score.

`models.py` holds `User` and `UserType` models. User types are validated before insertion, ensuring no invalid type values are saved. This enforces theoretical constraints at the database level.

### Routes and Forms
`routes.py` ties logic to the web interface:
- `/calculate`: users submit two types and a typology to get a result.
- `/register`: users choose their types from dynamically loaded lists of available typologies.

`forms.py` manages forms for registration, login, and profile editing. The form fields and validations are driven by the theoretical concepts implemented in the classes.

## Testing
Tests ensure the theory is correctly implemented:
- `tests/test_typologies.py`: checks typology logic — from retrieving types to determining relationships and handling errors.
- `tests/test_routes.py`: verifies user flows, including login, registration, language changes, and calculation endpoints.
- `tests/test_services.py`: ensures `calculate_relationship()` and `get_types_by_typology()` work as intended.
- `tests/test_models.py`: tests database logic and `UserType` validation.
- `tests/test_errors.py`: confirms correct handling of 404 and 500 errors.

A high test coverage (~93%) confirms that the theoretical ideas are correctly mirrored in code and thoroughly tested.

## Installation and Run

Prerequisites: Python 3.10+, Flask, pytest, and other dependencies listed in `requirements.txt`.

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest --maxfail=1 --disable-warnings -q

# Start the application (development mode)
export FLASK_APP=app
export FLASK_ENV=development
flask run
