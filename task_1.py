

def find_min_max(arr, start=0, end=None ):

    if end is None:
        end = len(arr) - 1

    if start == end:
        return (arr[start], arr[end])
    
    if end - start == 1:
        return (min(arr[start], arr[end]), max(arr[start], arr[end]))
    
    mid =  (start + end) // 2

    left_min, left_max = find_min_max(arr, start, mid)
    right_min, right_max = find_min_max(arr, mid + 1, end)

    return (min(left_min, right_min), max(left_max, right_max))

# Тест 1
print(find_min_max([5, 3, 8, 1, 9, 2, 7]))  # Очікується: (1, 9)

# Тест 2
print(find_min_max([42]))  # Очікується: (42, 42)

# Тест 3
print(find_min_max([10, -5]))  # Очікується: (-5, 10)