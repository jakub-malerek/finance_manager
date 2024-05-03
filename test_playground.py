class Test:
    def __init__(self, x, y):
        self.x = x
        self.y = y


t = Test(1, 2)

atrs = [atr for atr in dir(t) if not atr.startswith(
    "__") or not atr.startswith("_")]
print([e for e in ["x", "y", "c"] if e in atrs])
