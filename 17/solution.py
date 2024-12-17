class Computer():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.inst = 0

    def combo(self, x):
        return [0, 1, 2, 3, self.a, self.b, self.c, None][x]
    
    def adv(self, x):
        self.a = self.a // (2 ** self.combo(x))
        self.inst += 2

    def bxl(self, x):
        self.b = self.b ^ x
        self.inst += 2

    def bst(self, x):
        self.b = self.combo(x) % 8
        self.inst += 2

    def jnz(self, x):
        if self.a == 0:
            self.inst += 2
            return
        self.inst = x

    def bxc(self, x):
        self.b = self.b ^ self.c
        self.inst += 2

    def out(self, x):
        self.inst += 2
        return self.combo(x) % 8
    
    def bdv(self, x):
        self.b = self.a // (2 ** self.combo(x))
        self.inst += 2

    def cdv(self, x):
        self.c = self.a // (2 ** self.combo(x))
        self.inst += 2

    def run(self, program: list):
        output = []
        commands = [self.adv, self.bxl, self.bst, self.jnz,
                    self.bxc, self.out, self.bdv, self.cdv]
        while self.inst < len(program):
            cmd, operand = program[self.inst:self.inst+2]
            result = commands[cmd](operand)
            if result is not None:
                output.append(result)
        return output


with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        name, thing = line.split(':')
        match name:
            case 'Register A':
                a = int(thing)
            case 'Register B':
                b = int(thing)
            case 'Register C':
                c = int(thing)
            case 'Program':
                program = [int(x) for x in thing.split(',')]
            case _:
                raise ValueError(f'Unknown line: {line}')
            
computer = Computer(a, b, c)
output = computer.run(program)
output = ','.join(map(str, output))
print(f'Part 1: {output}')