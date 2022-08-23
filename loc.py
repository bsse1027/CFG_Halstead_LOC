commentSymbol = "#"
# fileToCheck = "/home/user/PycharmProjects/maintenence_tool/whiletest.py"


lineCount = 0
totalBlankLineCount = 0
totalCommentLineCount = 0

with open("whiletest.py") as f:
    fileLineCount = 0
    fileBlankLineCount = 0
    fileCommentLineCount = 0

    for line in f:
        lineCount += 1
        fileLineCount += 1

        lineWithoutWhitespace = line.strip()
        if not lineWithoutWhitespace:
            totalBlankLineCount += 1
            fileBlankLineCount += 1
        elif lineWithoutWhitespace.startswith(commentSymbol):
            totalCommentLineCount += 1
            fileCommentLineCount += 1

print('')
print('Totals')
print('--------------------')
print('Lines:         ' + str(lineCount))
print('Blank lines:   ' + str(totalBlankLineCount))
print('Comment lines: ' + str(totalCommentLineCount))
print('Code lines:    ' + str(lineCount - totalBlankLineCount - totalCommentLineCount))

# https://github.com/rrwick/LinesOfCodeCounter/blob/master/lines_of_code_counter.py
