# Psychological Calculator Project

**Table of Contents:**
1. [Project Description](#project-description)
2. [Repository Overview](#repository-overview)
   - [Key Components](#key-components)
   - [Getting Started](#getting-started)
   - [Next Steps for Exploration](#next-steps-for-exploration)
3. [Architecture Overview](#architecture-overview)
4. [Theoretical Foundations](#theoretical-foundations)
    - [Temporistics (Time)](#temporistics-time)
    - [Psychosophy (Personality Aspects)](#psychosophy-personality-aspects)
    - [Socionics (Modeling of Information)](#socionics-modeling-of-information)
5. [Implementation in Code](#implementation-in-code)
    - [Typology Classes](#typology-classes)
    - [Services and Data Validation](#services-and-data-validation)
    - [Routes and Forms](#routes-and-forms)
6. [Testing](#testing)
7. [Installation and Run](#installation-and-run)
    - [Local Run](#local-run)
    - [Running with Docker](#running-with-docker)
    - [Running Tests](#running-tests)
8. [Additional Information](#additional-information)

---

## Project Description

This project integrates theoretical concepts from several typologies (Temporistics, Psychosophy, Socionics, Amatoric, IQ, and Temperaments) and implements them in a web application. Users can select their types, calculate relationships between types, and view the "comfort score" of these interactions.

The main goal is to demonstrate how theoretical models of perception (time, personality aspects, information) can be transformed into practical code, tested thoroughly, and presented through a web interface.

> **Note for newcomers:** The typologies used in this project are exploratory models rather than a definitive scientific solution for human compatibility. They provide a framework for experiments and may be extended with new typologies in the future. If you're new to these concepts, see [HowThisIsWorkTogetherEN.md](HowThisIsWorkTogetherEN.md) for a beginner-friendly overview of each typology and where conflicts between them often arise.

## Repository Overview

This application is built with **Flask** and lets users choose psychological "types" from different typologies to calculate how compatible two types are.

### Key Components

- **App factory & configuration** (`create_app`, `run.py`) initialize Flask extensions, register blueprints, and configure optional OAuth providers.
- **Models** (`User`, `UserType` and OAuth token storage) store user data and validate type selections.
- **Routes & Forms** handle registration, login, profile editing, and relationship calculations.
- **Typology logic** in `app/typologies/` and helper functions in `services.py` implement the Temporistics, Psychosophy, and other rules.
- **Templates & Static Assets** under `app/templates/` provide the interface; translations live in `translations/` and `locales/`.
- **Tests** in `tests/` cover algorithms, routes, models, localization, and Selenium end-to-end cases with about 93% coverage.
- **Chat interface** (`/chat`) lets logged-in users talk to an OpenAI-powered assistant with optional voice input.

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

## Architecture Overview

The project follows a standard Flask blueprint structure with a dedicated service layer and typology modules.
For a detailed description and diagrams of how requests move through these components, see
[ARCHITECTURE.md](ARCHITECTURE.md).

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

### IQ Typology
- **Gentle levels:** Aspiring, Balanced, Insightful.
- Emphasizes how cognitive approaches influence compatibility.

### Temperament Typology
- **Classical types:** Sanguine, Choleric, Melancholic, Phlegmatic.
- Focuses on stable behavioral patterns and emotional responses.

## Implementation in Code

### Typology Classes
Under `app/typologies/`, each typology is implemented as a class derived from an abstract `Typology`. They provide methods like:
- `get_all_types()` to retrieve all types.
- `shorten_type()` to abbreviate type names.
- `determine_relationship_type()` to calculate the relationship type between two given types.
- `get_comfort_score()` to determine a "comfort score" based on their relationship.

These methods directly reflect the theoretical principles: induction/deduction (Temporistics), analysis/synthesis (Psychosophy), and modeling (Socionics).
The same interface now exposes additional typologies like `TypologyIQ` for IQ levels and `TypologyTemperaments` for classical temperaments.

### Typology Plugins
External packages can provide new typology implementations. The application uses
`stevedore` to discover modules that expose an entry point in the
`temporistics.typology` namespace. Each plugin module should import
`register_typology` from `app.typologies.registry` and call it during import to
register its classes. Once such a package is installed, its typologies become
available automatically at startup.

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
   # Chat configuration
   CHAT_PROVIDER=openai               # "openai", "huggingface", "gemini", "anthropic", "localhf"
   OPENAI_MODEL=gpt-3.5-turbo
   OPENAI_API_KEY=your-openai-key
   HUGGINGFACE_MODEL=google/flan-t5-small
   HUGGINGFACE_API_TOKEN=your-hf-token
   GEMINI_MODEL=gemini-pro
   GEMINI_API_KEY=your-gemini-key
   ANTHROPIC_MODEL=claude-3-haiku-20240307
   ANTHROPIC_API_KEY=your-anthropic-key
  LOCAL_MODEL_PATH=/path/to/local/model
  ```

To automate key changes, run `python rotate_secrets.py` which generates
new random values for the variables above and updates your `.env` file.
Add a monthly cron job, e.g. `0 0 1 * * /usr/bin/python /path/to/rotate_secrets.py`,
to rotate secrets regularly.

To fine‑tune compatibility values during research, use `adjust_comfort_score.py`:

```bash
python adjust_comfort_score.py Psychosophia "Identity/Philia" 75 --data-dir data
```

This updates the corresponding JSON file with the provided score.

3. **Run the development server**:

   Recommended approach using `run_local.sh`:
   ```bash
   chmod +x run_local.sh  # grant execute permission once
   ./run_local.sh
   ```

   The script automatically:
   - Ensures the PostgreSQL container is running
   - Exports DATABASE_URL with the container address
   - Runs the test suite before launch (unless --no-tests is used)
   - Starts the app on port 5001


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


### Updating translations

Run `make translations` whenever you change text in the templates or Python files:

```bash
make translations
```

This extracts messages with Babel, updates the `.po` catalogs in `translations/`, and compiles the binary files.

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

## Security and secret management

`config.py` relies on **Dynaconf** to load variables from a `.env` file and the
environment. While this is convenient for local development, production
deployments should store secrets in a dedicated vault such as **HashiCorp
Vault** or **AWS SSM**. Dynaconf will read these values from environment
variables, so no code changes are needed when switching to a secret manager.

The application uses **Flask‑Talisman** with a strict Content Security Policy
and HTTPS enabled by default. To disable HTTPS enforcement during local testing,
set `TALISMAN_FORCE_HTTPS=false` in your environment.

## Additional Information

This project is developed by [Your Name] and is licensed under the MIT License.

For more information, please visit the project repository on [GitHub](https://github.com/yourusername/psychological-calculator) or contact the developer at [your.email@example.com].
