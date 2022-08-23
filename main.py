from pycfg.pycfg import PyCFG, CFGNode, slurp
import argparse
import tkinter as tk
from PIL import ImageTk, Image
import sys
import math
global Vocabulary
Vocabulary = 0
operators = ["=", "+", "-", "*", "\\", "^", "\"", "\'", ".", "~", "|", "[", "]", "(", ")", ";", ":", "%", ",", "!", "<",
             ">", "&", "{", "}"]

operands = ["function", "global", "for", "end", "while", "if", "else", "elseif", "break", "switch", "case", "otherwise",
            "try", "catch", "end", "const", "import", "export", "type", "return",
            "true", "false", "in", "abstract", "module", "continue", "do", "join"]

singleLineComment = "#"
multilineCommentStart = "#="
multilineCommentEnd = "=#"

n1 = {}
n2 = {}


def filter_token(token):
    tok = token
    while tok:
        tok = break_token(tok)


def break_token(token):
    op_pos = len(token)
    for op in operators:
        if token.startswith(op):
            if op not in n1:
                n1[op] = 1
            else:
                n1[op] += 1
            return token[len(op):]
        if op in token:
            op_pos = min(op_pos, token.find(op))

    remaining_token = token[:op_pos]
    for keyword in operands:
        if remaining_token == keyword:
            if keyword not in n2:
                n2[keyword] = 1
            else:
                n2[keyword] += 1

    if remaining_token not in n2:
        n2[remaining_token] = 1
    else:
        n2[remaining_token] += 1

    return token[op_pos:]


def measure_halstead(N1, N2, n1, n2):
    global Vocabulary
    Vocabulary = n1 + n2
    Volume = (N1 + N2) * math.log(Vocabulary, 2)
    Difficulty = ((n1 / 2) * (N2 / n2))
    Effort = Difficulty * Volume

    print("Vocabulary: ", Vocabulary)
    print("Volume: ", Volume)
    print("Difficulty: ", Difficulty)
    print("Effort: ", Effort)


def filter_comments(sourceCodeFile):
    singleLineCommentPosition = -1
    multiLineCommentStartPosition = -1
    multiLineCommentEndPosition = -1
    linesWithoutComments = []
    isCommentWithinMultiLineComment = False
    with open(sourceCodeFile, 'r') as sourceFile:
        for line in sourceFile:
            if not line.strip():
                continue
            if singleLineComment in line:
                singleLineCommentPosition = line.find(singleLineComment)
            if multilineCommentStart in line:
                multiLineCommentStartPosition = line.find(multilineCommentStart)
            if multilineCommentEnd in line:
                multiLineCommentEndPosition = line.find(multilineCommentEnd)

            if not isCommentWithinMultiLineComment and singleLineCommentPosition != -1:
                linesWithoutComments.append(line[:singleLineCommentPosition])
            elif isCommentWithinMultiLineComment and multiLineCommentEndPosition != -1:
                isCommentWithinMultiLineComment = False
            elif multiLineCommentStartPosition != -1:
                isCommentWithinMultiLineComment = True
            elif isCommentWithinMultiLineComment:
                isCommentWithinMultiLineComment = True
            else:
                linesWithoutComments.append(line)

            singleLineCommentPosition = -1
            multiLineCommentStartPosition = -1
            multiLineCommentEndPosition = -1

    return linesWithoutComments


def main(sourcecode_file):
    lines = filter_comments(sourcecode_file)

    print("Lines of Code: ", len(lines))
    for line in lines:
        tokens = line.strip().split()
        for token in tokens:
            filter_token(token)

    for key, value in n1.items():
        print(key + " = " + str(value))

    for key, value in n2.items():
        print(key + " = " + str(value))

    print("Operator(n1): ", n1)
    print("Operand(n2): ", n2)
    measure_halstead(sum(n1.values()), sum(n2.values()), len(n1), len(n2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    argn = len(sys.argv)
    parser.add_argument('pythonfile')
    args = parser.parse_args()
    arcs = []
    main(args.pythonfile)

    cfg = PyCFG()
    cfg.gen_cfg(slurp(args.pythonfile).strip())
    g = CFGNode.to_graph(arcs)
    g.draw(args.pythonfile + '.png', prog='dot')

    # Tkinter.
    root = tk.Tk()
    root.title("Control Flow Graph")
    img1 = Image.open(str(args.pythonfile) + ".png")  # PIL solution
    img1 = img1.resize((800, 600), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img1)

    background = "red"

    panel = tk.Label(root, height=600, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    nodes = g.number_of_nodes()  # no. of nodes.
    edges = g.number_of_edges()  # no. of Edges.
    complexity = edges - nodes + 2  # Cyclomatic complexity

    frame = tk.Frame(root, bg=background)
    frame.pack(side="bottom", fill="both", expand="yes")

    tk.Label(frame, text="Nodes\t\t" + str(nodes), bg=background).pack()
    tk.Label(frame, text="Edges\t\t" + str(edges), bg=background).pack()
    tk.Label(frame, text="Cyclo Complexity\t" +
                         str(complexity), bg=background).pack()
    tk.Label(frame, text="Vocabulary\t\t" + str(Vocabulary), bg=background).pack()
    root.mainloop()

# https://www.geeksforgeeks.org/draw-control-flow-graph-using-pycfg-python/
