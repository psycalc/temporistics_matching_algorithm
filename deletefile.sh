#!/bin/bash

# Настройки
REMOTE_NAME="origin"  # Имя удалённого репозитория
SIZE_THRESHOLD=75MB    # Порог размера файлов для удаления (измените по необходимости)

# Функция для конвертации размера в байты
convert_size_to_bytes() {
    local size=$1
    local number=$(echo $size | grep -o -E '[0-9]+')
    local unit=$(echo $size | grep -o -E '[A-Za-z]+')

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

# Проверка наличия Git
if ! command -v git &> /dev/null
then
    echo "Git не установлен. Установите Git и повторите попытку."
    exit 1
fi

# Проверка, находится ли скрипт в корне Git-репозитория
if [ ! -d ".git" ]; then
    echo "Скрипт должен быть запущен из корневой директории Git-репозитория."
    exit 1
fi

# Проверка наличия незафиксированных изменений
if [ -n "$(git status --porcelain)" ]; then
    echo "Обнаружены незафиксированные изменения. Выполняется git stash..."
    git stash save "pre-filter-repo stash - $(date +"%Y-%m-%d %H:%M:%S")"
    STASHED=true
else
    STASHED=false
fi

echo "Поиск файлов размером более $SIZE_THRESHOLD в истории репозитория..."

# Конвертация порога размера в байты
SIZE_THRESHOLD_BYTES=$(convert_size_to_bytes $SIZE_THRESHOLD)

# Поиск больших файлов в истории
LARGE_FILES=$(git rev-list --objects --all | \
    git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
    grep '^blob' | \
    awk -v threshold=$SIZE_THRESHOLD_BYTES '$3 >= threshold {print $4 " " $3}' | \
    sort -k2 -nr)

if [ -z "$LARGE_FILES" ]; then
    echo "Не найдено файлов, превышающих порог $SIZE_THRESHOLD."
    # Восстановление стэша, если он был создан
    if [ "$STASHED" = true ]; then
        git stash pop
    fi
    exit 0
fi

echo "Найдены следующие большие файлы:"
echo "$LARGE_FILES"

# Подтверждение удаления
read -p "Вы хотите удалить эти файлы из истории? [y/N]: " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Отмена операции."
    # Восстановление стэша, если он был создан
    if [ "$STASHED" = true ]; then
        git stash pop
    fi
    exit 0
fi

# Извлечение путей файлов для удаления
FILES_TO_REMOVE=$(echo "$LARGE_FILES" | awk '{print $1}')

# Создание резервной ветки
BACKUP_BRANCH="backup-$(date +%Y%m%d%H%M%S)"
echo "Создаётся резервная ветка: $BACKUP_BRANCH"
git branch $BACKUP_BRANCH

# Удаление файлов из истории с помощью git filter-repo
echo "Удаление файлов из истории..."
for FILE in $FILES_TO_REMOVE
do
    git filter-repo --path "$FILE" --invert-paths
done

# Проверка результатов
echo "Проверка, что большие файлы удалены..."
CHECK_LARGE_FILES=$(git rev-list --objects --all | \
    git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
    grep '^blob' | \
    awk -v threshold=$SIZE_THRESHOLD_BYTES '$3 >= threshold {print $4 " " $3}')

if [ -z "$CHECK_LARGE_FILES" ]; then
    echo "Удаление успешно. Больших файлов больше нет в истории."
else
    echo "Предупреждение: Некоторые большие файлы всё ещё присутствуют:"
    echo "$CHECK_LARGE_FILES"
fi

# Принудительная отправка изменений
read -p "Вы хотите принудительно отправить изменения на удалённый репозиторий '$REMOTE_NAME'? [y/N]: " push_confirm
if [[ "$push_confirm" =~ ^[Yy]$ ]]; then
    echo "Отправка изменений..."
    git push --force --all $REMOTE_NAME
    git push --force --tags $REMOTE_NAME
    echo "История успешно переписана и отправлена на удалённый репозиторий."
else
    echo "Принудительная отправка отменена. Не забудьте самостоятельно отправить изменения, когда будете готовы."
fi

# Восстановление стэша, если он был создан
if [ "$STASHED" = true ]; then
    echo "Восстановление сохранённых изменений из стэша..."
    git stash pop
fi

echo "Операция завершена."
