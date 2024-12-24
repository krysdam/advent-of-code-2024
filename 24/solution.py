class Wire():
    """A wire, with a string name, boolean value, and int level.
    
    The level is the number of steps from the input.
    Input wires (xNN and yNN) have level 0,
    wires that depend only on input wires have level 1,
    wires that depend on wires with level k have level k+1.
    """
    def __init__(self, name, value=None, level=None):
        self.name = name
        self.value = value
        self.level = level

    def __str__(self):
        s = f'{self.name}={self.value}'
        if self.level is not None:
            s += f'(l{self.level})'
        return s
    
    def __repr__(self):
        return str(self)
    

class Gate():
    """A gate, with two input Wires, an output Wire, and a function op.
    
    Gates also have levels. A gate's level is the level of its output.
    For example a gate that depends only on input wires (which have level 0)
    would itself have output level 1, and therefore have level 1 itself.
    """
    def __init__(self, in1, in2, op, out, level=None):
        self.in1 = in1
        self.in2 = in2
        self.op = op
        self.out = out
        self.level = None # A gate has the level of its output

    def apply(self):
        result = self.op( self.in1.value, self.in2.value)
        self.out.value = result

    def __str__(self):
        opname = OPERATOR_NAMES[self.op]
        s = f'[{self.in1.name} {opname} {self.in2.name} --> {self.out.name}]'
        s += f' @ l{self.level}'
        return s
    
    def __repr__(self):
        return str(self)

# The operators and their names
AND = lambda a, b: a and b
OR  = lambda a, b: a  or b
XOR = lambda a, b: a  ^  b
OPERATORS = {'AND': AND, 'OR': OR, 'XOR': XOR}
OPERATOR_NAMES = {AND: 'AND', OR: 'OR', XOR: 'XOR'}

# Collect the wires and gates from the file.
wires = {}
gates = []
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # Input wires (the first part of the file)
        if ':' in line:
            name, value = line.split(': ')
            value = int(value)
            wire = Wire(name, value=value, level=0)
            wires[name] = wire
        
        # Gates (the second part of the file)
        else:
            in1, op, in2, _, out = line.split(' ')
            in1, in2 = sorted([in1, in2])
            if in1 not in wires:
                wires[in1] = Wire(in1)
            if in2 not in wires:
                wires[in2] = Wire(in2)
            if out not in wires:
                wires[out] = Wire(out)
            # For the moment, a Gate's input and output are strings.
            # In a moment we'll replace them with the Wires themselves.
            gates.append( Gate(in1, in2, OPERATORS[op], out) )

# Replace the Gate's Wire properties with actual Wires
for gate in gates:
    gate.in1 = wires[gate.in1]
    gate.in2 = wires[gate.in2]
    gate.out = wires[gate.out]

# Iterate over all gates to assign a level to every wire and gate.
all_have_levels = False
highest_level = 0
while not all_have_levels:
    all_have_levels = True
    for gate in gates:
        in1_level = gate.in1.level
        in2_level = gate.in2.level
        if in1_level is None or in2_level is None:
            all_have_levels = False
        else:
            out_level = max(in1_level, in2_level) + 1
            gate.out.level = out_level
            gate.level = out_level
            highest_level = max(highest_level, out_level)

# Uncomment lines here to print the parts of the device.
for level in range(highest_level+1):
    for gate in sorted(gates, key = lambda g: str(g)):
        if gate.level == level:
            gate.apply()
            #print(gate)
    #for wirename in wires:
    #    wire = wires[wirename]
    #    if wire.level == level:
    #        print(wire)
   #print()

def bits_to_number(bits):
    """Convert the list of bits (little-endian) to an int."""
    bits.reverse()
    result = 0
    for bit in bits:
        result *= 2
        result += bit
    return result


# Part 1: What is the current output of the device?
zwires = [wires[name] for name in wires if name[0] == 'z']
zwires.sort(key = lambda w: w.name)
zbits = [wire.value for wire in zwires]
znum = bits_to_number(zbits)
print(f'Part 1: {znum}')


# Part 2: What four pairs of output wires are swapped?
# Doing this in the general case may be intractible.
# Certainly, doing it for only one input manually
# is easier than designing a general algorithm.

# I used the printing code above to find the right swaps.
# The device has basically two steps, similar to gradeschool arithmetic.
# Imagine the two input numbers x and y one over the other.
# The first step is to find the XOR (sum) and AND (carry) of each column.
# The second step is to "cascade" these carries to the left,
# finding one more bit of the answer per iteration.

# One swap put z10 into the "sum and carry" step instead of step 2.
# --> Swap z10 and vcf

# One swap made z17 the output of an AND instead of the corresponding XOR.
# --> Swap z17 and fhg

# One swap put z39 one iteration layer than it should be.
# --> Swap z39 and tnc

# One swap swapped a "sum" and "carry" result in the same column.
# --> Swap fsq and dvb

# Sort these
swaps = ['z10', 'vcf', 'z17', 'fhg', 'z39', 'tnc', 'fsq', 'dvb']
code = ','.join(sorted(swaps))
print(f'Part 2: {code}')
print('NOTE: This part 2 answer was found manually.',
      'It is only correct for some inputs.')