from functools import partial, reduce


def log(*args):
    out = reduce(lambda acc, s: acc + " " + s, args)
    color = '\033[106m'
    nocolor = '\033[0m'
    print("{color}log{nocolor} {out}".format(color=color, out=out,
                                             nocolor=nocolor))


def logInFile(fileName, fnName="-"):
    return partial(log, "[{file}] {fn} >>>>".format(file=fileName, fn=fnName))
