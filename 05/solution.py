# Extract the rules and updates from the input file

rules = []   # List of tuples (before, after)
updates = [] # List of lists [page, page, page...]

with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        # Skip the one blank line
        if not line:
            continue

        # Lines like X|Y are rules
        if '|' in line:
            before, after = line.split('|')
            before = int(before)
            after = int(after)
            rules.append((before, after))

        # Other lines are updates
        else:
            update = [int(x) for x in line.split(',')]
            updates.append(update)


def does_conform(update, rule):
    """Does the update follow the rule?"""
    before, after = rule
    try:
        return update.index(before) < update.index(after)
    except ValueError:
        return True
    
def middle_value(update):
    """Return the middle value of the update. Assumes odd length."""
    return update[len(update) // 2]


def compare_by_rules(page1, page2):
    """Compare the page order according to all the rules."""
    for rule in rules:
        before, after = rule
        if page1 == before and page2 == after:
            return True
    return False

class Page():
    def __init__(self, number):
        self.number = number

    def __gt__(self, other):
        return compare_by_rules(self.number, other.number)


total_already_correct = 0
total_need_correction = 0
for update in updates:
    # Part 1: Total of the middle values of updates that already follow the rules
    if all(does_conform(update, rule) for rule in rules):
        total_already_correct += middle_value(update)
    # Part 2: Total of the middle values of updates that need correction
    else:
        # Make the update a list of Page objects
        update = [Page(x) for x in update]
        # Sort the update (which will sort according to the rules)
        update.sort()
        # Convert back to a list of ints
        update = [x.number for x in update]
        # Now add the middle value
        total_need_correction += middle_value(update)

print(f"Part 1: {total_already_correct}")
print(f"Part 2: {total_need_correction}")