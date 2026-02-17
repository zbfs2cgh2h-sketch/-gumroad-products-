# Top 10 Python One-Liners Cheat Sheet 🚀

**Save hours of debugging with these production-ready snippets**

---

## 1. Flatten Nested Lists
```python
flat = [item for sublist in nested_list for item in sublist]
# Example: [[1,2], [3,4]] → [1,2,3,4]
```

## 2. Remove Duplicates (Preserve Order)
```python
unique = list(dict.fromkeys(my_list))
# Faster than set() for small lists, keeps order
```

## 3. Transpose Matrix
```python
transposed = list(zip(*matrix))
# [[1,2], [3,4]] → [(1,3), (2,4)]
```

## 4. Read File Lines into List
```python
lines = [line.strip() for line in open('file.txt')]
# No need to close, handles newlines
```

## 5. Count Occurrences
```python
from collections import Counter
counts = Counter(my_list)
# Returns: {'apple': 3, 'banana': 2}
```

## 6. Swap Dictionary Keys/Values
```python
swapped = {v: k for k, v in my_dict.items()}
# Assumes unique values
```

## 7. Get Multiple Dict Values
```python
values = [my_dict.get(k, default) for k in keys]
# Safe extraction with defaults
```

## 8. Check if Any/All Conditions Met
```python
any_true = any(x > 10 for x in numbers)
all_true = all(x > 0 for x in numbers)
```

## 9. Merge Dictionaries (Python 3.9+)
```python
merged = dict1 | dict2
# Faster than {**dict1, **dict2}
```

## 10. HTTP Request with Error Handling
```python
import requests; data = requests.get(url, timeout=5).json() if requests.get(url, timeout=5).ok else {}
```

---

## Bonus: Time Your Code
```python
import timeit; print(f"{timeit.timeit(lambda: your_function(), number=1000):.4f}s")
```

---

**Want more?** Check out my Dev.to profile for full tutorials: https://dev.to/zbfs2cgh2h

**Need custom Python solutions?** DM me or grab my advanced guides on Gumroad.

---

© 2026 | No AI fluff, just code that works.
