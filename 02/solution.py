def first_differences(report: list):
    """The first differences of the sequence."""
    diffs = []
    for n1, n2 in zip(report, report[1:]):
        diffs.append(n2 - n1)
    return diffs

def is_safe(report: list):
    """Is the report safe? (Monotonic and increments are 1, 2, or 3)"""
    diffs = set(first_differences(report))
    if diffs.issubset({1, 2, 3}):
        return True
    if diffs.issubset({-1, -2, -3}):
        return True
    return False

def is_safe_fault_tolerant(report: list):
    """Is the report safe, after at most one level is removed?"""
    for i in range(len(report)):
        pruned = report[:i] + report[i+1:]
        if is_safe(pruned):
            return True
    return False

# Count the safe reports
safe_count = 0
safe_fault_tolerant_count = 0

with open("input.txt", "r") as file:
    for line in file:
        line = line.strip()
        report = list(map(int, line.split()))

        # Check if the report is safe
        if is_safe(report):
            safe_count += 1
        if is_safe_fault_tolerant(report):
            safe_fault_tolerant_count += 1

print(f"Part 1: {safe_count}")
print(f"Part 2: {safe_fault_tolerant_count}")