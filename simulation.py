''' Runs simulation of 4chan boxes picture '''

from random import randint

def main():
    ''' Randomly chooses a 'ball' from a 'box'. If it is gold, validTrials is
    incremented and another ball is taken. If it is also gold, success is
    incremented '''
    boxes = [['gold', 'gold'], ['gold', 'silver'], ['silver', 'silver']]
    trials = 10**5
    valid = 0
    success = 0
    for x in range(trials):
        box = boxes[randint(0, 2)]
        ball_one = randint(0, 1)
        if box[ball_one] == 'gold':
            valid += 1
            ball_two = (ball_one + 1) % 2
            if box[ball_two] == 'gold':
                success += 1
    print(success / valid)

if __name__ == "__main__":
    main()
