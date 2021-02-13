from functools import partial, reduce


def log(*args):
    out = reduce(lambda acc, s: acc + " " + s, args)
    print("log {}".format(out))


def logInFile(fileName, fnName="-"):
    return partial(log, "[{file}] {fn} >>>>".format(file=fileName, fn=fnName))
