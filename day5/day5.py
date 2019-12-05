class VM:
    def __init__(self, memory, input_val):
        self.input = input_val
        self.memory = memory
        self.pc = 0
        self.register = [0,0,0]
        self.halt_requested = False
        self.opcodes = { # function, # of params, # of params we care about paramter mode (assumption last is storage)
            1: (self.add, 3, 2),
            2: (self.mul, 3, 2),
            3: (self.save, 1, 0),
            4: (self.output, 1, 1),
            5: (self.jump_if_true, 2, 2),
            6: (self.jump_if_false, 2, 2),
            7: (self.less_than, 3, 2),
            8: (self.equals, 3, 2),
            99: (self.halt, 0, 0)
        }

    def add (self):
        self.memory[self.register[2]] = self.register[0] + self.register[1]

    def mul (self):
        self.memory[self.register[2]] = self.register[0] * self.register[1]

    def save(self):
        self.memory[self.register[0]] = self.input

    def output(self):
        print(F"OUTPUT: {self.register[0]}")        

    def equals(self):
        self.memory[self.register[2]] = 1 if self.register[0] == self.register[1] else 0
    
    def less_than(self):
        self.memory[self.register[2]] = 1 if self.register[0] < self.register[1] else 0

    def jump_if_true(self):
        if self.register[0] != 0:
            self.pc = self.register[1]        

    def jump_if_false(self):
        if self.register[0] == 0:
            self.pc = self.register[1]        

    def halt(self):
        self.halt_requested = True

    def read(self):
        pc = self.pc
        self.pc += 1
        return self.memory[pc]

    def load(self, reg_num, mode):
        val = self.read()
        if mode == 0:
            val = self.memory[val]        
        self.register[reg_num] = val

    def run(self):
        while not self.halt_requested:
            op = self.read()
            op_code = op % 100
            
            fn, param_count, param_mode_count = self.opcodes[op_code]
            for x in range(param_count):
                param_mode = ((op // pow(10,x+2)) % 10)
                self.load(x, param_mode if x < param_mode_count else 1)

            fn()
    
with open("input.txt") as data:
    codes = [int(x) for x in data.readline().strip().split(",")]

print (f"Part1: ")
machine = VM(codes.copy(), 1)
machine.run()
print (f"Part2: ")
machine = VM(codes.copy(), 5)
machine.run()
