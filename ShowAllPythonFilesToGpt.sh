#!/bin/bash
echo "Additional info: This project deals with crypt features."
find . -type f -name "*.py" \
  -not -path "*/venv/*" \
  -not -path "*/.git/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/env/*" \
  -not -path "*/site-packages/*" \
  -exec sh -c 'for f; do
    if [ "$(file -b --mime-type "$f")" = "text/x-python" ]; then
      echo "F:$f:"
      cat "$f"
    fi
  done' sh {} + \
| awk 'BEGIN{q=0} {if(index($0,"\"\"\"")>0){q=!q;next} if(!q)print}' \
| tr '\n' ' ' \
| sed 's/  */ /g'
