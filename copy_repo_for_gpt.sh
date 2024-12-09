#!/usr/bin/env bash

# This script prepares code and related files for a GPT model prompt.
#
# Features:
# - By default, searches the current directory (.) for .py files.
# - Can include other file types via --include-file-types (e.g., "*.html Dockerfile").
# - Joins all code into one line (keeps comments, empty lines, docstrings).
# - Copies the final result to the clipboard by default (if pbcopy or xclip are available).
# - Splits the output into multiple parts if needed.
# - Prints a "DO NOT ANSWER YET" message before all parts, and "YOU MAY NOW START ANSWERING." after all parts.
# - Shows a user prompt at the end (`--user-prompt`).
# - If insufficient information is provided, the model should suggest parameters for re-running the script.
# - `--show-structure` displays the project structure before output.
# - `--include-dirs` allows specifying which directories to include in the search.
# - `--solution-format full|lines` instructs how the final solution should be presented (full file or just changed lines).
#
# Additional improvements:
# - Each file's content is preceded by a line indicating the relative file path: ">>>FILE: path/to/file<<<"
# - More detailed instructions are added to the final prompt about how to use the script and its parameters.
#
# Usage Examples:
#   ./copy_repo_for_gpt.sh
#   ./copy_repo_for_gpt.sh --include-file-types "*.html Dockerfile"
#   ./copy_repo_for_gpt.sh --show-structure
#   ./copy_repo_for_gpt.sh --include-dirs "app templates"
#   ./copy_repo_for_gpt.sh --solution-format lines
#   ./copy_repo_for_gpt.sh --user-prompt "How can I improve CI/CD?"
#
# Parameters:
#   --include-file-types : Specify additional filenames/extensions (e.g. "*.html Dockerfile docker-compose.yml").
#   --show-structure     : Show directory structure before outputting code parts.
#   --include-dirs       : Space-separated directories to search in (default is ".").
#   --solution-format    : "full" or "lines". Default "full".
#
# If the model cannot help with the given info, it should suggest how to re-run the script with more parameters.

CLIPBOARD=true
CHUNK_SIZE=15000
INCLUDE_FILE_TYPES=()
USER_PROMPT=""
SHOW_STRUCTURE=false
INCLUDE_DIRS=()
SOLUTION_FORMAT="full"

ORIGINAL_PARAMS=("$@")

while (( "$#" )); do
  case "$1" in
    --include-file-types)
      shift
      IFS=' ' read -r -a INCLUDE_FILE_TYPES <<< "$1"
      shift
      ;;
    --user-prompt)
      shift
      USER_PROMPT="$1"
      shift
      ;;
    --show-structure)
      SHOW_STRUCTURE=true
      shift
      ;;
    --include-dirs)
      shift
      IFS=' ' read -r -a INCLUDE_DIRS <<< "$1"
      shift
      ;;
    --solution-format)
      shift
      SOLUTION_FORMAT="$1"
      shift
      ;;
    *)
      echo "Unknown parameter: $1"
      exit 1
      ;;
  esac
done

# If no dirs specified, use current dir
if [ ${#INCLUDE_DIRS[@]} -eq 0 ]; then
  SEARCH_PATHS=(".")
else
  SEARCH_PATHS=("${INCLUDE_DIRS[@]}")
fi

EXCLUDE_PATHS=(
  -not -path "*/venv/*"
  -not -path "*/.git/*"
  -not -path "*/__pycache__/*"
  -not -path "*/env/*"
  -not -path "*/site-packages/*"
)

# By default, we look for Python files
FIND_EXPRS=(-name "*.py")

# If additional file types are specified, we add them with OR conditions:
if [ ${#INCLUDE_FILE_TYPES[@]} -gt 0 ]; then
  NEW_FIND_EXPRS=()
  for ft in "${INCLUDE_FILE_TYPES[@]}"; do
    NEW_FIND_EXPRS+=(-o -name "$ft")
  done
  FIND_EXPRS=( \( "${FIND_EXPRS[@]}" "${NEW_FIND_EXPRS[@]}" \) )
else
  FIND_EXPRS=( \( "${FIND_EXPRS[@]}" \) )
fi

# If --show-structure is true, show a filtered tree of the project structure.
if $SHOW_STRUCTURE; then
  echo ">>>PROJECT STRUCTURE (EXCLUDING COMMON DIRS)<<<"
  for d in "${SEARCH_PATHS[@]}"; do
    echo "Directory: $d"
    find "$d" "${EXCLUDE_PATHS[@]}" | sed 's/^\.\///' | awk '{
      level = gsub(/\//,"/",$0);
      for (i=0; i<level; i++) printf "  ";
      print $0
    }'
  done
  echo ">>>END OF PROJECT STRUCTURE<<<"
  echo
fi

RESULT=$(
  find "${SEARCH_PATHS[@]}" -type f "${EXCLUDE_PATHS[@]}" "${FIND_EXPRS[@]}" \
    -exec sh -c '
      for f; do
        rel_path=$(realpath --relative-to="$(pwd)" "$f")
        echo ">>>FILE: $rel_path<<<"
        cat "$f" | tr "\n" " " | sed "s/  */ /g"
        echo " "
      done
    ' sh {} +
)

# Trim leading/trailing spaces
RESULT=$(echo "$RESULT" | sed 's/^ *//;s/ *$//')

# Build the additional prompt with parameters
ADDITIONAL_PROMPT="ADDITIONAL PROMPT:\nThis code was prepared by the script \`$0\` with parameters:\n"
ADDITIONAL_PROMPT+="\`$0 ${ORIGINAL_PARAMS[*]}\`\n"
ADDITIONAL_PROMPT+="If the provided information is insufficient, please suggest how to re-run the script with different parameters.\n"

# Add instructions for solution format
SOLUTION_INSTRUCTION=""
if [ "$SOLUTION_FORMAT" = "full" ]; then
  SOLUTION_INSTRUCTION="Please provide the final solution by showing the entire modified file(s)."
elif [ "$SOLUTION_FORMAT" = "lines" ]; then
  SOLUTION_INSTRUCTION="Please provide the final solution by showing only the specific lines that need to be changed."
else
  SOLUTION_INSTRUCTION="Please provide the final solution by showing the entire modified file."
fi

# Add a HOW TO USE section
HOW_TO_USE=$(cat <<EOF

HOW TO USE THIS SCRIPT:

- Basic usage:
  ./copy_repo_for_gpt.sh

- Include additional file types:
  ./copy_repo_for_gpt.sh --include-file-types "*.html Dockerfile"

- Show project structure before code:
  ./copy_repo_for_gpt.sh --show-structure

- Restrict search to certain directories:
  ./copy_repo_for_gpt.sh --include-dirs "app templates"

- Change solution format (how the model should present final solution):
  ./copy_repo_for_gpt.sh --solution-format lines

This script collects code from specified directories, merges them into a single line of text, and provides instructions for the GPT model on how to answer. If you find the information insufficient, consider re-running the script with more directories, file types, or enabling structure display.

EOF
)

FINAL_OUTPUT="$RESULT

$ADDITIONAL_PROMPT

USER PROMPT:
$USER_PROMPT

$SOLUTION_INSTRUCTION

$HOW_TO_USE

If you cannot help with the provided info, please suggest how to re-run this script with different parameters (e.g., '--include-file-types', '--show-structure', '--include-dirs', '--solution-format', '--user-prompt' or other arguments) to make the provided information more complete.
"

# Copy to clipboard if available
if $CLIPBOARD; then
    if command -v pbcopy &> /dev/null; then
        echo "$FINAL_OUTPUT" | pbcopy
    elif command -v xclip &> /dev/null; then
        echo "$FINAL_OUTPUT" | xclip -sel clip
    else
        echo "No clipboard command found. Please install pbcopy (macOS) or xclip (Linux)."
    fi
fi

LENGTH=${#FINAL_OUTPUT}
TOTAL_PARTS=$(( (LENGTH + CHUNK_SIZE - 1) / CHUNK_SIZE ))

echo ">>>BEGIN MULTI-PART PROMPT<<<"
echo "DO NOT ANSWER YET. WAIT UNTIL ALL PARTS ARE PROVIDED."
echo

PART=1
START=0
while [ $START -lt $LENGTH ]; do
  END=$((START + CHUNK_SIZE))
  if [ $END -gt $LENGTH ]; then
    END=$LENGTH
  fi
  CHUNK="${FINAL_OUTPUT:$START:$((END-START))}"
  echo "[PART $PART of $TOTAL_PARTS]"
  echo "$CHUNK"
  echo
  START=$END
  PART=$((PART+1))
done

echo ">>>END OF LAST PART<<<"
echo "YOU MAY NOW START ANSWERING."
