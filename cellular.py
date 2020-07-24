''' Given starting pattern and rule, display generations of one-dimensional
cellular automaton '''

from time import sleep

def main():
    ''' Take user input and display generations '''
    rule = int(input("Rule: "))
    rule = format(rule, '08b')[-8:]
    current = input("Start pattern: ")
    iters = int(input("Iterations: "))
    if len(current) < 2:
        current = '0'+current+'0'
    for x in range(iters, 0, -1):
        pad = '0' * x
        print_gen(pad+current+pad)
        current = find_next_gen(rule, '0'+current+'0')
        sleep(0.1)

def find_next_gen(rule, current):
    ''' Return next generation '''
    check = ['111', '110', '101', '100', '011', '010', '001', '000']
    next_gen = ''
    length = len(current)
    for x in range(length):
        if x == 0:
            nhood = '0' + current[x:x+2]
        elif x == length - 1:
            nhood = current[x-1:x+1] + '0'
        else:
            nhood = current[x-1:x+2]
        index = check.index(nhood)
        next_gen += rule[index]
    return next_gen

def print_gen(current):
    ''' Print the current generation using ANSI codes '''
    for cell in current:
        if cell == '1':
            print("\033[0;47m \033[0m", end='')
        else:
            print("\033[0;0m \033[0m", end='')
    print()

if __name__ == "__main__":
    main()
