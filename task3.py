import timeit

def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

def compute_lps(pattern):
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

def kmp_search(text, pattern):
    M, N = len(pattern), len(text)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1

def rabin_karp(text, pattern, q=101):
    m, n = len(pattern), len(text)
    if m == 0:
        return -1
    d = 256
    p = t = 0
    h = 1
    for i in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t and text[i:i + m] == pattern:
            return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return -1

# Read files
file1_path = "article1.txt"
file2_path = "article2.txt"

with open(file1_path, encoding="utf-8") as f:
    text1 = f.read()

with open(file2_path, encoding="utf-8") as f:
    text2 = f.read()

pattern_existing = "алгоритми"
pattern_fabricated = "неіснуючийпідрядок"

results = {"Article 1": {}, "Article 2": {}}

for text, article in zip([text1, text2], ["Article 1", "Article 2"]):
    for algo_name, algo in [
        ("Boyer-Moore", boyer_moore),
        ("Knuth-Morris-Pratt", kmp_search),
        ("Rabin-Karp", rabin_karp),
    ]:
        for substring_type, substring in [
            ("Existing", pattern_existing),
            ("Fabricated", pattern_fabricated),
        ]:
            time_taken = timeit.timeit(lambda: algo(text, substring), number=10)
            results[article][f"{algo_name} ({substring_type})"] = time_taken

for article, timings in results.items():
    print(f"Results for {article}:")
    for desc, time in timings.items():
        print(f"  {desc}: {time:.6f} seconds")
