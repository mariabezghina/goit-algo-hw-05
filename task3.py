import timeit
import random
import string
from typing import List

# Алгоритм Кнута-Морріса-Пратта
def kmp_search(pattern: str, text: str) -> List[int]:
    def compute_lps(pattern: str) -> List[int]:
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    lps = compute_lps(pattern)
    i = j = 0
    result = []
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            result.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result

# Алгоритм Боєра-Мура
def bm_search(pattern: str, text: str) -> List[int]:
    def build_bad_char_table(pattern: str):
        bad_char = [-1] * 256
        for i in range(len(pattern)):
            bad_char[ord(pattern[i])] = i
        return bad_char
    
    m, n = len(pattern), len(text)
    bad_char = build_bad_char_table(pattern)
    s = 0
    result = []
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            result.append(s)
            s += (m - bad_char[ord(text[s + m])] if s + m < n else 1)
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
    return result

# Алгоритм Рабіна-Карпа
def rk_search(pattern: str, text: str, q=101) -> List[int]:
    d = 256
    m, n = len(pattern), len(text)
    p = t = 0
    h = 1
    result = []
    for i in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                result.append(i)
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return result

# Читання текстових файлів
with open("article1.txt", "r", encoding="utf-8") as file:
    text1 = file.read()
with open("article2.txt", "r", encoding="utf-8") as file:
    text2 = file.read()

# Вибір підрядків
existing_substring = text1[:20]
non_existing_substring = "".join(random.choices(string.ascii_letters, k=20))

# Функція для вимірювання часу виконання

def measure_time(algorithm, pattern, text):
    return timeit.timeit(lambda: algorithm(pattern, text), number=10)

# Вимірювання часу
algorithms = {"KMP": kmp_search, "BM": bm_search, "RK": rk_search}
results = {}

for algo_name, algo_func in algorithms.items():
    results[(algo_name, "article1", "existing")] = measure_time(algo_func, existing_substring, text1)
    results[(algo_name, "article1", "non_existing")] = measure_time(algo_func, non_existing_substring, text1)
    results[(algo_name, "article2", "existing")] = measure_time(algo_func, existing_substring, text2)
    results[(algo_name, "article2", "non_existing")] = measure_time(algo_func, non_existing_substring, text2)

# Виведення результатів
for key, value in results.items():
    print(f"Algorithm: {key[0]}, Text: {key[1]}, Substring type: {key[2]}, Time: {value:.6f} sec")
