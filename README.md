# Psychological Calculator Project

**Table of Contents:**
1. [Project Description](#project-description)
2. [Repository Overview](#repository-overview)
   - [Key Components](#key-components)
   - [Getting Started](#getting-started)
   - [Next Steps for Exploration](#next-steps-for-exploration)
3. [Theoretical Foundations](#theoretical-foundations)
    - [Temporistics (Time)](#temporistics-time)
    - [Psychosophy (Personality Aspects)](#psychosophy-personality-aspects)
    - [Socionics (Modeling of Information)](#socionics-modeling-of-information)
4. [Implementation in Code](#implementation-in-code)
    - [Typology Classes](#typology-classes)
    - [Services and Data Validation](#services-and-data-validation)
    - [Routes and Forms](#routes-and-forms)
5. [Testing](#testing)
6. [Installation and Run](#installation-and-run)
    - [Local Run](#local-run)
    - [Running with Docker](#running-with-docker)
    - [Running Tests](#running-tests)
7. [Additional Information](#additional-information)

---

## Project Description

This project integrates theoretical concepts from three typologies (Temporistics, Psychosophy, and Socionics) and implements them in a web application. Users can select their types, calculate relationships between types, and view the "comfort score" of these interactions.

The main goal is to demonstrate how theoretical models of perception (time, personality aspects, information) can be transformed into practical code, tested thoroughly, and presented through a web interface.

## Repository Overview

This application is built with **Flask** and lets users choose psychological "types" from different typologies to calculate how compatible two types are.

### Key Components

- **App factory & configuration** (`create_app`, `run.py`) initialize Flask extensions, register blueprints, and configure optional OAuth providers.
- **Models** (`User`, `UserType` and OAuth token storage) store user data and validate type selections.
- **Routes & Forms** handle registration, login, profile editing, and relationship calculations.
- **Typology logic** in `app/typologies/` and helper functions in `services.py` implement the Temporistics, Psychosophy, and other rules.
- **Templates & Static Assets** under `app/templates/` provide the interface; translations live in `translations/` and `locales/`.
- **Tests** in `tests/` cover algorithms, routes, models, localization, and Selenium end-to-end cases with about 93% coverage.

### UX/UI Improvements

Recent updates introduce accessibility and responsive design best practices:

- Added `<meta charset>` and viewport tags for mobile-friendly rendering.
- Navigation now uses semantic roles and supports keyboard skipping with a "Skip to main content" link.
- Flash messages announce updates with `role="alert"` for screen readers.
- Inputs feature placeholder text, and styles adapt to smaller screens.
- The interface now loads **Bootstrap 5** for consistent styling across forms and navigation.

### Getting Started

1. Install dependencies: `pip install -r requirements.txt`.
2. Create a `.env` file or rely on the defaults in `config.py`.
3. Run `./run_local.sh` and open `http://localhost:5001/` in your browser.

### Next Steps for Exploration

- Review `app/__init__.py` to understand how blueprints are registered.
- Study the typology algorithms in `app/typologies/`.
- Look into OAuth configuration in `app/oauth.py`.
- Explore the test suite under `tests/` for usage examples.
- Check `translations/` to see how localization is added.

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

### Local Run

1. **Preparation**:
   - Ensure Python 3.10 or newer is installed
   - Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment setup**:
   - Create a `.env` file in the project root if it does not exist
   - Configure the necessary environment variables, for example:
   ```
   FLASK_CONFIG=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///site.db  # SQLite is fine for local usage
   BABEL_DEFAULT_LOCALE=en
   BABEL_DEFAULT_TIMEZONE=Europe/Kiev
   LANGUAGES=en,fr,es,uk
   ```

3. **Run the development server**:

   Recommended approach using `run_local.sh`:
   ```bash
   chmod +x run_local.sh  # grant execute permission once
   ./run_local.sh
   ```

   The script automatically:
   - Sets up the environment for SQLite (database created in the project root)
   - Creates required directories
   - Checks write permissions for the database file
   - Initializes the database if it does not exist
   - Starts the app on port 5001 to avoid conflicts

   Alternative direct run:
   ```bash
   python run.py
   ```

   The application will be available at http://localhost:5001 when using the script or http://localhost:5000 when started directly.

   > **Possible issues and solutions**:
   >
   > 1. **PostgreSQL connection error** – if you cannot connect to host `db`, use `run_local.sh` or set `DATABASE_URL` to SQLite.
   > 2. **Port already in use** – either change `FLASK_RUN_PORT` in `run_local.sh` or stop the process using `sudo lsof -i :5000` and `sudo kill <PID>`.
   > 3. **SQLite "unable to open database file"** – check directory permissions (`ls -la`), run the latest script to create the DB, or try running with elevated privileges `sudo ./run_local.sh`.

### Running with Docker

1. **Using Docker Compose**:
   ```bash
   docker-compose up
   ```
   This command starts PostgreSQL and the web application.

2. **Run only the web application**:
   ```bash
   docker-compose up web
   ```

### Running Tests

#### Common commands

1. **Set up the test environment**:
   ```bash
   export PYTHONPATH="$PYTHONPATH:$(pwd)"
   export USE_TEST_DB_URL="sqlite:///test.db"
   export FLASK_CONFIG=testing
   ```

2. **Run all tests**:
   ```bash
   python -m pytest
   ```

3. **Run a specific test**:
   ```bash
   python -m pytest tests/test_localization.py::test_language_affects_content
   ```

4. **Run tests from a particular file**:
   ```bash
   python -m pytest tests/test_models.py
   ```

5. **Run tests with verbose output**:
   ```bash
   python -m pytest -xvs tests/test_localization.py
   ```

6. **Run Selenium tests**:
   ```bash
   python -m pytest -m selenium
   ```

   Make sure you have Chrome and a matching ChromeDriver installed for Selenium tests.

#### Alternative Selenium script

You can also run Selenium tests with:
```bash
bash run_selenium_tests.sh
```

#### Running tests in Docker

```bash
docker-compose up test
```

#### Testing notes

- SQLite is used instead of PostgreSQL during tests to avoid external dependencies.
- Temporary tables are created and removed during test runs.
- If you change the database structure, update the tests accordingly.
- High coverage (~93%) confirms the theoretical ideas are well reflected in code.

## Additional Information

This project is developed by [Your Name] and is licensed under the [License Name].

For more information, please visit the project repository on [GitHub](https://github.com/yourusername/psychological-calculator) or contact the developer at [your.email@example.com].
