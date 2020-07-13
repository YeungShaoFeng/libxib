from random import randint as random_randint
from random import shuffle as random_shuffle
from random import choice as random_choice
from time import sleep as time_sleep


# snap a little bit
# 1.3 -- 3.6
def rest():
    snap = [random_randint(1, 3), random_randint(1, 3), random_randint(1, 3)]
    ndigit = [random_randint(1, 3), random_randint(1, 3), random_randint(1, 3)]
    random_shuffle(ndigit)
    choice = random_choice([0, 1, 2, 3, 4, 5])
    if choice == 0:
        snap = (
            snap[0] / (ndigit[ndigit[0] - 1])
            + snap[1] / (10 ** ndigit[ndigit[1] - 1])
            + snap[2] / (10 ** ndigit[ndigit[2] - 1])
        )
    elif choice == 1:
        snap = (
            snap[0] / (ndigit[ndigit[0] - 1])
            + snap[2] / (10 ** ndigit[ndigit[1] - 1])
            + snap[1] / (10 ** ndigit[ndigit[2] - 1])
        )
    elif choice == 2:
        snap = (
            snap[1] / (ndigit[ndigit[0] - 1])
            + snap[0] / (10 ** ndigit[ndigit[1] - 1])
            + snap[2] / (10 ** ndigit[ndigit[2] - 1])
        )
    elif choice == 3:
        snap = (
            snap[1] / (ndigit[ndigit[0] - 1])
            + snap[2] / (10 ** ndigit[ndigit[1] - 1])
            + snap[0] / (10 ** ndigit[ndigit[2] - 1])
        )
    elif choice == 4:
        snap = (
            snap[2] / (ndigit[ndigit[0] - 1])
            + snap[0] / (10 ** ndigit[ndigit[1] - 1])
            + snap[1] / (10 ** ndigit[ndigit[2] - 1])
        )
    elif choice == 5:
        snap = (
            snap[0] / (ndigit[ndigit[0] - 1])
            + snap[1] / (10 ** ndigit[ndigit[1] - 1])
            + snap[0] / (10 ** ndigit[ndigit[2] - 1])
        )
    snap = round(snap, ndigit[choice % 3])
    if snap < 1.5:
        snap += 1
    time_sleep(snap)
