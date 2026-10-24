import simplejson as json
import sys
import os

CELLSIZE="1.8cm"
SOLCELLSIZE="0.9cm"

MIN_ANSWER_SIZE=3

BLANK_CLUE = "(blank clue)"

translate = {
    "en": {
        "crossword puzzle": "Crossword Puzzle",
        "title": "Title",
        "by": "by",
        "author": "Author",
        "created": "Created",
        "solution": "Solution",
        "across": "Across",
        "down": "Down",
    },
    "pt": {
        "crossword puzzle": "Palavra Cruzada",
        "title": "Título",
        "by": "por",
        "author": "Autor",
        "created": "Criado em",
        "solution": "Solução",
        "across": "Horizontais",
        "down": "Verticais",
    },
}

def to_latex(data, language):
#   Paint black cells
#    "  cell{{1}{5}} = {bg=black},"
#    "  cell{{2}{5}} = {bg=black},"
    black_cells = ""
    N = data['size']['rows']
    M = data['size']['cols']

    for i in range(N):
        for j in range(M):
            if data['grid'][M*i+j]=='.':
                black_cells += "cell{{"+str(i+1)+"}"+"{"+str(j+1)+"}} = {bg=black},"

#   Helper functions and lists
    def size_at_least_min(i,j,direction):
        if direction == 'across':
            for x in range(MIN_ANSWER_SIZE):
                if not valid(i,j+x):
                    return False
        else:
            for x in range(3):
                if not valid(i+x,j):
                    return False
        return True

    clues_by_number = {
            'across':[],
            'down':[],
    }
    for direction in ['across','down']:
        for entry in data['clues'][direction]:
            number, _, clue = entry.partition('. ')
            number = int(number)
            clues_by_number[direction].append([number,clue])

    def valid(i,j):
        return i>=0 and i<N and j>=0 and j<M and data['grid'][M*i+j]!='.'
    def check_clue(clue_id,direction):
        for [number,clue] in clues_by_number[direction]:
            if number == clue_id:
                return True
        return False
    def is_blank(clue_id):
        for [number,clue] in clues_by_number['across']:
            if number == clue_id:
                if clue != BLANK_CLUE:
                    return False
        for [number,clue] in clues_by_number['down']:
            if number == clue_id:
                if clue != BLANK_CLUE:
                    return False
        return True
    def set_blank(clue_id,direction):
        for entry in clues_by_number[direction]:
            [number,clue] = entry
            if number == clue_id:
                entry[1] = BLANK_CLUE
    def is_clue(i,j,clue_id):
        return valid(i,j) and ((not valid(i-1,j) and check_clue(clue_id,'down')) or (not valid(i,j-1) and check_clue(clue_id,'across')))
    def is_clue_dir(i,j,clue_id,direction):
        if direction == 'across':
            return valid(i,j) and (not valid(i,j-1) and check_clue(clue_id,'across'))
        else:
            return valid(i,j) and (not valid(i-1,j) and check_clue(clue_id,'down'))

#   Clue numbers on grid and circles
    written_numbers = ""
    clue_cnt = 0
    for i in range(N):
        for j in range(M):
            if is_clue(i,j,clue_cnt+1):
                clue_cnt += 1

#               Filter clues with size less than 3
                for direction in ['across','down']:
                    if is_clue_dir(i,j,clue_cnt,direction) and not size_at_least_min(i,j,direction):
                        set_blank(clue_cnt,direction)

                if is_blank(clue_cnt):
                    written_numbers += "\\textsuperscript{ }"
                    if 'circles' in data and data['circles'][M*i+j] == 1:
                        written_numbers += "\\put(20.5,-9.5){\\circle{\\cellsize}}"
                else:
                    written_numbers += "\\textsuperscript{"+str(clue_cnt)+"}"
                    if 'circles' in data and data['circles'][M*i+j] == 1:
                        written_numbers += "\\put(18.5,-9){\\circle{\\cellsize}}"
            else:
                written_numbers += "\\textsuperscript{ }"
                if 'circles' in data and data['circles'][M*i+j] == 1:
                    written_numbers += "\\put(20.5,-9.5){\\circle{\\cellsize}}"
            written_numbers += " & " if j < M-1 else "\\\\ \n"

#    Clues
#    "        \\item[1] Clue 1\n"
#    "        \\item[5] Clue 5\n"
#    "        \\item[6] Clue 6\n"
    clue_desc = {
            'across':"",
            'down':"",
    }
    for direction in ['across','down']:
        for [number,clue] in sorted(clues_by_number[direction]):
            if clue != BLANK_CLUE:
                clue_desc[direction] += "\\item["+str(number)+"] "+clue.replace('_','\\_').replace('&nbsp;',' ')+"\n"

#    Solution
#    "         \\textbf{S}  & \\textbf{O} & \\textbf{L} & \\textbf{ } & \\textbf{ } \\\\\n"
    solution = ""
    for i in range(N):
        for j in range(M):
            solution += "\\textbf{"+data['grid'][M*i+j]+"}"
            solution += " & " if j < M-1 else "\\\\ \n"
    ret = ((
        "\\begin{center}\n"
        "\n"
        "{\n"
        "\\huge{"+translate[language]['title']+"}\\\\\n"
        "\\LARGE{"+data['title']+"}\\\\\n"
        "\\vspace{0.3cm}\n"
        "\\Large{"+translate[language]['by']+" "+data['author']+"}\n"
        "}\n"
        "\n"
        "\\vspace{0.3cm}\n"
        "\n"
        "\\begin{table}[H]\n"
        "\\centering\n"
        "\\begin{tblr}{\n"
        "  colspec = {"+"X[l,h,\\cellsize]"*data['size']['cols']+"},\n"
        "  stretch = 0,\n"
        "  rowsep = 2pt,\n"
        "  row{1-"+str(data['size']['rows'])+"} = {\\cellsize - 4pt, font=\\LARGE\\bfseries},\n"
        "  colsep = 0.1pt,\n"
        "  hlines = {black, 1.2pt},\n"
        "  vlines = {black, 1.2pt},\n"
        "  "+black_cells+""
        "}\n"
        ""+written_numbers+""
        "    \\end{tblr}\n"
        "    \\label{crossword}\n"
        "\\end{table}\n"
        "\n"
        "\\vspace{0.2cm}\n"
        "\n"
        "\\begin{multicols}{2}\n"
        "    {\\Large "+translate[language]['across']+"}\n"
        "    \\begin{enumerate}\n"
        "    \\large\n"
        ""+clue_desc['across']+""
        "    \\end{enumerate}\n"
        "    \n"
        "    \\columnbreak\n"
        "    \n"
        "    {\\Large "+translate[language]['down']+"}\n"
        "    \\begin{enumerate}\n"
        "    \\large\n"
        ""+clue_desc['down']+""
        "    \\end{enumerate}\n"
        "\\end{multicols}\n"
        "\n"
        "\\vspace{0.3cm}\n"
        ""+translate[language]['created']+" \\today\n"
        "\\end{center}\n"),(
        "\\begin{center}\n"
        "{\n"
        "\\huge{"+translate[language]['solution']+" - "+data['title']+"}\n"
        "}\n"
        "\n"
        "\\begin{table}[H]\n"
        "\\centering\n"
        "\\rotatebox[origin=c]{180}{\n"
        "\\begin{tblr}{\n"
        "  colspec = {"+"X[c,m,\\solcellsize]"*data['size']['cols']+"},\n"
        "  stretch = 0,\n"
        "  rowsep = 2pt,\n"
        "  row{1-"+str(data['size']['rows'])+"} = {\\solcellsize - 4pt, font=\\Large\\bfseries},\n"
        "  colsep = 0.1pt,\n"
        "  hlines = {black, 1.2pt},\n"
        "  vlines = {black, 1.2pt},\n"
        "  "+black_cells+""
        "}\n"
        ""+solution+""
        "    \\end{tblr}\n"
        "    }\n"
        "    \\label{crossword}\n"
        "\\end{table}\n"
        "\n"
        "\\end{center}\n"
        ))
    return ret

def main():
    if len(sys.argv) < 2:
        print("Usage: "+sys.argv[0]+" [-o outfile] [-p] infile...")
        sys.exit(1)

    language = "en"

    for arg in sys.argv:
        if arg[0] != '-':
            continue
        if arg == "-p":
            language = "pt"

    outfile = "a"

    babel = ""
    if language == "pt":
        babel = "\\usepackage[portuguese]{babel}\n"

    cat_cw = (
        "\\documentclass[a4paper]{article}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage[table]{xcolor}\n"
        "\\usepackage{tabularray}  \n"
        "\\usepackage{float}\n"
        "\\usepackage{multicol}\n"
        "\\usepackage{pict2e}\n"
        ""+babel+""
        "\\title{"+translate[language]['crossword puzzle']+"}\n"
        "\\author{"+translate[language]['author']+"}\n"
        "\\date{\\today}\n"
        "\n"
        "\\begin{document}\n"
        "\\pagenumbering{gobble}\n"
        "\n"
        "\\def\\cellsize{"+CELLSIZE+"}\n"
        "\\def\\solcellsize{"+SOLCELLSIZE+"}\n"
    )
    cat_sol = cat_cw

    i = 1
    while i < len(sys.argv):
        if sys.argv[i][0] == '-':
            if sys.argv[i] == "-o":
                outfile = sys.argv[i+1]
                i += 2
                continue
            if sys.argv[i] == "-p":
                language = "pt"
                i += 1
                continue
            print("Error: unknown option '-"+sys.argv[i][1:]+"'")
            sys.exit(1)

        infile = sys.argv[i]
        if not os.path.exists(infile):
            print("Error: file '"+sys.argv[i]+"' does not exist")
            sys.exit(1)

        with open(infile, 'r') as f:
            data = json.load(f)
            for field in ['author','title','size','clues','grid']:
                if not field in data:
                    print("Error (invalid input): field '"+field+"' not present in file "+str(i)+" ("+infile+").")
                    sys.exit(1)
            for direction in ['rows','cols']:
                if not direction in data['size']:
                    print("Error (invalid input): field 'size["+direction+"]' not present in file "+str(i)+" ("+infile+").")
                    sys.exit(1)
            for direction in ['across','down']:
                if not direction in data['clues']:
                    print("Error (invalid input): field 'clues["+direction+"]' not present in file "+str(i)+" ("+infile+").")
                    sys.exit(1)

            cw, sol = to_latex(data, language)
            cat_cw += cw
            cat_sol += sol

        cat_cw += "\\newpage"
        i += 1

    cat_cw += (
        "\n"
        "\\end{document}\n"
    )

    cat_sol += (
        "\n"
        "\\end{document}\n"
    )

    with open(outfile+'-cw.tex', 'w') as f:
        f.write(cat_cw)
    with open(outfile+'-sol.tex', 'w') as f:
        f.write(cat_sol)

if __name__ == "__main__":
    main()

