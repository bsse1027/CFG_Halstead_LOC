import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from pycfg.pycfg import PyCFG, CFGNode, slurp
import argparse
from PIL import Image
from PIL.ImageQt import ImageQt
from qtconsole.qt import QtCore

import sys
import math
import os
import radon

global Vocabulary
global Volume
global Difficulty
global Effort
global linesLen
global LLOC
global SLOC
Vocabulary = 0
Volume = 0
Difficulty = 0
Effort = 0
linesLen = 0

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
    global Vocabulary, Volume, Difficulty, Effort
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
    global linesLen,LLOC,SLOC
    count = 0
    lines = os.popen('radon hal ' + sourcecode_file).read()
    LOC = os.popen('radon raw ' + sourcecode_file).read()
    for line in LOC.split('\n'):
        if 'LOC' in line:
            count = count+1
            if count == 1:
                linesLen = line
            elif count == 2:
                LLOC = line
                print(LLOC)
            elif count == 3:
                SLOC = line
                print(SLOC)

        elif 'Comments' in line:
            print(line)
        elif 'Single comments' in line:
            print(line)
        elif 'Blank' in line:
            print(line)
    for line in lines.split('\n'):
        if 'h1' in line:
            print(line)
        if 'h2' in line:
            print(line)
        if 'N1' in line:
            print(line)
        if 'N2' in line:
            print(line)
        if 'vocabulary' in line:
            global Vocabulary
            Vocabulary = line
        if 'volume' in line:
            global Volume
            Volume = line
        if 'difficulty' in line:
            global Difficulty
            Difficulty = line
        if 'effort' in line:
            global Effort
            Effort = line

    # global linesLen
    # lines = filter_comments(sourcecode_file)
    #
    # # print("Lines of Code: ", len(lines))
    # linesLen = len(lines)
    #
    # for line in lines:
    #     tokens = line.strip().split()
    #     for token in tokens:
    #         filter_token(token)
    #
    # for key, value in n1.items():
    #     print(key + " = " + str(value))
    #
    # for key, value in n2.items():
    #     print(key + " = " + str(value))
    #
    # print("Operator(n1): ", n1)
    # print("Operand(n2): ", n2)
    # measure_halstead(sum(n1.values()), sum(n2.values()), len(n1), len(n2))


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\nControl Flow Graph \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')
        # self.resize(self, 800, 600)

    def setPixmap(self, image):
        super().setPixmap(image)


class Label(QLabel):
    def __init__(self):
        super().__init__()


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout()

        self.photoViewer = ImageLabel()
        self.label1 = Label()
        self.label2 = Label()
        self.label3 = Label()
        self.label4 = Label()
        self.label5 = Label()
        self.label6 = Label()
        self.label7 = Label()
        self.label8 = Label()
        self.label9 = Label()
        self.label10 = Label()

        mainLayout.addWidget(self.photoViewer)
        mainLayout.addWidget(self.label1)
        mainLayout.addWidget(self.label2)
        mainLayout.addWidget(self.label3)
        mainLayout.addWidget(self.label4)
        mainLayout.addWidget(self.label5)
        mainLayout.addWidget(self.label6)
        mainLayout.addWidget(self.label7)
        mainLayout.addWidget(self.label8)
        mainLayout.addWidget(self.label9)
        mainLayout.addWidget(self.label10)
        self.setLayout(mainLayout)

    # def set_image(self, file_path):
    #     self.photoViewer.setPixmap(file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    argn = len(sys.argv)
    parser.add_argument('pythonfile', help='The python file to be analyzed')
    args = parser.parse_args()
    arcs = []
    main(args.pythonfile)
    cfg = PyCFG()
    cfg.gen_cfg(slurp(args.pythonfile).strip())
    g = CFGNode.to_graph(arcs)
    g.draw(args.pythonfile + '.png', prog='dot')
    nodes = g.number_of_nodes()  # no. of nodes.
    edges = g.number_of_edges()  # no. of Edges.
    complexity = edges - nodes + 2
    app = QApplication(sys.argv)
    demo = AppDemo()
    x = (str(args.pythonfile) + ".png")
    print(x)
    img1 = Image.open(str(args.pythonfile) + ".png")
    print(img1.size)# PIL solution
    img1 = img1.resize((1080, 720), Image.ANTIALIAS)
    img1 = ImageQt(img1)
    demo.photoViewer.setPixmap(QPixmap.fromImage(img1))
    # demo.set_image(str(args.pythonfile) + ".png")
    demo.label1.setText("Nodes\t\t" + str(nodes))
    demo.label2.setText("Edges\t\t" + str(edges))
    demo.label3.setText("C.Complexity\t" + str(complexity))
    demo.label4.setText("Vocabulary\t" + str(Vocabulary))
    demo.label5.setText("Volume\t\t" + str(Volume))
    demo.label6.setText("Difficulty\t" + str(Difficulty))
    demo.label7.setText("Effort\t\t" + str(Effort))
    demo.label8.setText("LOC\t\t" + str(linesLen))
    demo.label9.setText("LLOC\t\t" + str(LLOC))
    demo.label10.setText("SLOC\t\t" + str(SLOC))
    demo.show()
    sys.exit(app.exec_())
