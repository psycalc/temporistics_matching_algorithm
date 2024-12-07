#!/bin/bash

# Указываем путь к вашему проекту (текущая директория по умолчанию)
PROJECT_DIR="."

# Функция для ввода пользователем папок, которые нужно включить
read -p "Введите через пробел названия папок, которые нужно включить (или нажмите Enter для всех): " -a INCLUDE_DIRS

# Проверяем, были ли указаны папки
if [ "${#INCLUDE_DIRS[@]}" -gt 0 ]; then
    # Формируем аргументы для find с учетом указанных папок
    INCLUDE_PATTERNS=""
    for DIR in "${INCLUDE_DIRS[@]}"; do
        if [ -n "$INCLUDE_PATTERNS" ]; then
            INCLUDE_PATTERNS+=" -o "
        fi
        INCLUDE_PATTERNS+=" -path \"$PROJECT_DIR/$DIR/*\""
    done
    FIND_CMD="find \"$PROJECT_DIR\" -type f -name \"*.py\" \\( $INCLUDE_PATTERNS \\)"
else
    # Если папки не указаны, ищем во всех пользовательских директориях
    FIND_CMD="find \"$PROJECT_DIR\" -type f -name \"*.py\" -not \( \
        -path \"*/venv/*\" -o \
        -path \"*/.git/*\" -o \
        -path \"*/__pycache__/*\" \)"
fi

# Выполняем команду find
eval "$FIND_CMD -print0" | while IFS= read -r -d '' file; do
    echo "=== Содержимое файла: $file ==="
    cat "$file"
    echo
done
