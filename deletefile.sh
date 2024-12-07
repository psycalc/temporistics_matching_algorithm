#!/bin/bash

# Settings
REMOTE_NAME="origin"    # Remote repository name
SIZE_THRESHOLD="75MB"   # File size threshold

# Function to convert size to bytes
convert_size_to_bytes() {
    local size=$1
    local number=$(echo "$size" | grep -o -E '[0-9]+')
    local unit=$(echo "$size" | grep -o -E '[A-Za-z]+')

    case "$unit" in
        KB|kb)
            echo $((number * 1024))
            ;;
        MB|mb)
            echo $((number * 1024 * 1024))
            ;;
        GB|gb)
            echo $((number * 1024 * 1024 * 1024))
            ;;
        B|b)
            echo $number
            ;;
        *)
            echo "0"
            ;;
    esac
}

# Check for Git installation
if ! command -v git &> /dev/null
then
    echo "Git is not installed. Please install Git and rerun."
    exit 1
fi

# Check if script runs in the root of a Git repo
if [ ! -d ".git" ]; then
    echo "This script must be run from the root of a Git repository."
    exit 1
fi

# Stash changes if there are any unstaged modifications
if [ -n "$(git status --porcelain)" ]; then
    echo "Uncommitted changes found. Stashing changes..."
    git stash save "pre-filter-repo stash - $(date +"%Y-%m-%d %H:%M:%S")"
    STASHED=true
else
    STASHED=false
fi

echo "Searching for files larger than $SIZE_THRESHOLD in repository history..."

# Convert threshold to bytes
SIZE_THRESHOLD_BYTES=$(convert_size_to_bytes "$SIZE_THRESHOLD")

# Find large files in history
LARGE_FILES=$(git rev-list --objects --all | \
    git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
    grep '^blob' | \
    awk -v threshold=$SIZE_THRESHOLD_BYTES '$3 >= threshold {print $4 " " $3}' | \
    sort -k2 -nr)

if [ -z "$LARGE_FILES" ]; then
    echo "No files found exceeding $SIZE_THRESHOLD."
    # Restore stash if created
    if [ "$STASHED" = true ]; then
        git stash pop
    fi
    exit 0
fi

echo "The following large files were found:"
echo "$LARGE_FILES"

read -p "Do you want to remove these files from the history? [y/N]: " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Operation canceled."
    # Restore stash if created
    if [ "$STASHED" = true ]; then
        git stash pop
    fi
    exit 0
fi

# Extract file paths
FILES_TO_REMOVE=$(echo "$LARGE_FILES" | awk '{print $1}')

# Create a backup branch
BACKUP_BRANCH="backup-$(date +%Y%m%d%H%M%S)"
echo "Creating backup branch: $BACKUP_BRANCH"
git branch "$BACKUP_BRANCH"

echo "Removing files from history using git-filter-repo..."

# Build the filter-repo arguments for all files
FILTER_ARGS=()
for FILE in $FILES_TO_REMOVE; do
    FILTER_ARGS+=("--path" "$FILE")
done

# Run git filter-repo once with all files
git filter-repo --force --invert-paths "${FILTER_ARGS[@]}"

# Verify removal
echo "Verifying that large files have been removed..."
CHECK_LARGE_FILES=$(git rev-list --objects --all | \
    git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
    grep '^blob' | \
    awk -v threshold=$SIZE_THRESHOLD_BYTES '$3 >= threshold {print $4 " " $3}')

if [ -z "$CHECK_LARGE_FILES" ]; then
    echo "Removal successful. No large files remain in the history."
else
    echo "Warning: Some large files are still present:"
    echo "$CHECK_LARGE_FILES"
fi

read -p "Do you want to forcibly push the rewritten history to the '$REMOTE_NAME' remote? [y/N]: " push_confirm
if [[ "$push_confirm" =~ ^[Yy]$ ]]; then
    echo "Forcibly pushing changes..."
    git push --force --all "$REMOTE_NAME"
    git push --force --tags "$REMOTE_NAME"
    echo "History successfully rewritten and pushed to the remote repository."
else
    echo "Force push canceled. Remember to manually push when ready."
fi

# Restore stashed changes if any
if [ "$STASHED" = true ]; then
    echo "Restoring stashed changes..."
    git stash pop
fi

echo "Operation completed."
