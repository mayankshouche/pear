import sys
import scanner

# TODO: refactor into class so globals don't have to dangle

# globals
errorState = False

def main():
    args = sys.argv
    if len(args) > 2:
        print("Too many arguments!\nUsage: pear <filename>")
        sys.exit(-1)
    elif len(args) == 2:
        runSrc(args[1])
    else:
        repl()

def runSrc(file: str) -> None:
    code = None
    # TODO: add file error handling capabilites
    with open(file) as f:
        code = f.read()
    run(code)
    if(errorState):
        sys.exit(-1)

def repl() -> None:
    nextln = input(">>> ")
    while (nextln):
        run(nextln)
        errorState = False 
        nextln = input(">>> ")

def run(src: str) -> None:
    # TODO: make a static Scanner for REPL
    _scanner = scanner.Scanner(src)
    tokens = _scanner.getTokens()

    for t in tokens:
        print(t)

def err(line: int, message: str) -> None:
    print("Error! [line " + str(line) + "]: ", message)


if __name__ == "__main__":
    main()