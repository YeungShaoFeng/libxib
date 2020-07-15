from random import randint as random_randint
from random import shuffle as random_shuffle
from random import choice as random_choice
from time import sleep as time_sleep


def rest(base=None, gain=1.0, gap=[]) -> None:
    """
    snap a little bit\n
    [1.3-3.6]s + base\n
    :param base: base time line.
    :param gain: The amplifier.
    :param gap: snap + random  in the gap
    """
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
    if base:
        snap += base
    if gain != 1:
        snap *= gain
    if len(gap) > 1:
        snap += random_choice(gap)
    print("Now resting for {}s... ".format(snap), end='')
    time_sleep(snap)
    print("Done. ")
