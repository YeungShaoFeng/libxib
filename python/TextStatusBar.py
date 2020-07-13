class TextStatusBar:
    def __init__(self, scale):
        self.scale = scale
        self.length = 50
        self.cnt = 0

    def show(self, onlyOpercets=False, indentation=""):
        self.cnt += 1
        percents = self.cnt / self.scale
        pound = int(percents * self.length)
        space = int(self.length - pound)
        a = "#" * pound
        b = " " * space
        c = (self.cnt / self.scale) * 100
        if indentation != "":
            if onlyOpercets:
                print("{:^3.0f}%".format(c), end="")
            else:
                print("\r{}[{}{}] {:^3.0f}%".format(indentation, a, b, c), end="")
        else:
            print("\r[{}{}] {:^3.0f}%".format(a, b, c), end="")