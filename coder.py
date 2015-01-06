#!/usr/bin/env python3

import sys, tty, termios, csv

def getchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getargs():
    if len(sys.argv) < 3:
        print("Usage: coder input.file output.file")
        sys.exit()
    return sys.argv[1:3]

# def openfiles(infile, outfile):
#     files = open(infile, 'r'), open(outfile, 'w')
#     return files

def chooseheader(headers, prompt):
    chosen = -1
    while chosen > len(headers) or chosen <0:
        userinput = input(prompt)
        try:
            chosen = int(userinput)
# Input is a number
        except ValueError:
# Input is a string
            try:
                chosen = headers.index(userinput)
# Selectian is an existing column
            except ValueError:
# Selection is a new column
                chosen = len(headers)
    if chosen == len(headers):
        header = userinput
    else:
        header = headers[chosen]
    return chosen, header
                

def main():
    infile, outfile = getargs()
# Setup csv input and output
    with open(infile, 'r') as csvin, open(outfile, 'w') as csvout:
        datareader = csv.reader(csvin, delimiter = ',')
        datawriter = csv.writer(csvout, delimiter = ',')
# Print header info
        headerrow = next(datareader)
        print("Existing headers in file")
        i = 0
        for header in headerrow:
            print(i, '-' , header)
            i += 1

# Ask the user for the input column
        inputcol = len(headerrow)
        while inputcol >= len(headerrow):
            inputcol, _ = chooseheader(headerrow, "Choose input column: ")
            if inputcol == len(headerrow):
                print("Invalid selection")

# Ask the user for the output column
        outputcol, outputhead = chooseheader(headerrow, "Choose output column: ")

# Confirm selections with the user and write header row to output file
        inputchoice = "Input column: " + headerrow[inputcol]
        if outputcol == len(headerrow):
            outputchoice = "Output column: " + outputhead + " (new)"
            datawriter.writerow(headerrow + [outputhead])
        else:
            outputchoice = "Output column: " + headerrow[outputcol]
            datawriter.writerow(headerrow)
        print(inputchoice, ", ", outputchoice)

# Get possible column values
        outputvals = []
        valueprompt = ""
        userinput = input("Choose possible output values (leave blank to finish)\n1: ")
        while userinput != "":
            outputvals.append(userinput)
            valueprompt += str(len(outputvals)) + ": " + userinput + "   "
            userinput = input(str(len(outputvals) + 1)+": ")
        valueprompt += "(0 to flag. q to quit, saving progress)"

# Process the data
        i = 0
        while True:
            try:
                i += 1
                newrow = next(datareader)
                print("\n============== Item " + str(i) + " ==============\n")
                print(newrow[inputcol])
                print("\n" + valueprompt)
                while True:
                    try:
                        ch = getchar()
                        userinput = int(ch)
                        response = outputvals[userinput - 1]
                        break
                    except ValueError:
                        if ch == 'q':
                            sys.exit()
                        print("Numbers only")
                    except IndexError:
                        if userinput == 0:
                            break
                        else:
                            print("Invalid")
                if userinput == 0:
                    response = "FLAG!!!"
                print(response)
                if outputcol == len(headerrow):
                    newrow.append(response)
                else:
                    newrow[outputcol] = response
                datawriter.writerow(newrow)
            except StopIteration:
                break

if __name__ == "__main__":
    main()
