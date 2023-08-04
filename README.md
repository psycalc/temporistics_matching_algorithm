## Алгоритм

1. Якщо у обох користувачів в першій позиції однаковий аспект типології, тип відносин – "філія".
2. Якщо у користувачів співпадають другий та третій аспекти типології, тип відносин – "агапе".
3. Якщо перший аспект типології одного користувача співпадає з третім аспектом іншого (або навпаки), тип відносин – "ерос".
4. Якщо другий аспект типології одного користувача співпадає з четвертим аспектом іншого (або навпаки), тип відносин – "ерос".

Після визначення типу відносин, обчислюємо комфортність відносин на основі типу:

- Філія: комфортність = 2
- Агапе: комфортність = 4
- Ерос: комфортність = -2

## Приклад коду Python

```python
def relation_type(user1, user2):
    if user1[0] == user2[0]:
        return "Філія"
    if user1[1] == user2[1] and user1[2] == user2[2]:
        return "Агапе"
    if user1[0] == user2[2] or user1[2] == user2[0]:
        return "Ерос"
    if user1[1] == user2[3] or user1[3] == user2[1]:
        return "Ерос"

def comfort_score(relation_type):
    if relation_type == "Філія":
        return 2
    if relation_type == "Агапе":
        return 4
    if relation_type == "Ерос":
        return -2

# Приклад використання
user1 = ['typologyAspect1', 'typologyAspect2', 'typologyAspect3', 'typologyAspect4']
user2 = ['typologyAspect4', 'typologyAspect3', 'typologyAspect2', 'typologyAspect1']

relation_type = relation_type(user1, user2)
comfort_score = comfort_score(relation_type)
print(relation_type, comfort_score)
