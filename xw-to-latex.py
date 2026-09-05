import simplejson as json
import sys

N = 5
M = 5

def to_latex(data):
#   Paint black cells
#    "  cell{{1}{5}} = {bg=black},"
#    "  cell{{2}{5}} = {bg=black},"
    black_cells = ""
    for i in range(N):
        for j in range(M):
            if data['grid'][M*i+j]=='.':
                black_cells += "cell{{"+str(i+1)+"}"+"{"+str(j+1)+"}} = {bg=black},"

#   Clue numbers on grid and circles
    def valid(i,j):
        return i>=0 and i<N and j>=0 and j<M and data['grid'][M*i+j]!='.'
    def is_clue(i,j):
        return valid(i,j) and (not valid(i-1,j) or not valid(i,j-1))
    written_numbers = ""
    clue_cnt = 0
    for i in range(N):
        for j in range(M):
            if is_clue(i,j):
                clue_cnt += 1
                written_numbers += "\\textsuperscript{"+str(clue_cnt)+"}"
                if 'circles' in data and data['circles'][M*i+j] == 1:
                    written_numbers += "\\put(16.5,-11){\\circle{\\cellsize}}"
            else:
                written_numbers += "\\textsuperscript{ }"
                if 'circles' in data and data['circles'][M*i+j] == 1:
                    written_numbers += "\\put(17,-11){\\circle{\\cellsize}}"
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
        for entry in sorted(data['clues'][direction]):
            number, _, clue = entry.partition('. ')
            clue_desc[direction] += "\\item["+number+"] "+clue.replace('_','\\_').replace('&nbsp;',' ')+"\n"

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
        "\\huge{"+data['title']+"}\\\\\n"
        "\\LARGE{Theme - General}\\\\\n"
        "\\vspace{0.3cm}\n"
        "\\Large{by "+data['author']+"}\n"
        "}\n"
        "\n"
        "\\vspace{1cm}\n"
        "\n"
        "\\def\\cellsize{1.5cm}\n"
        "\\def\\solcellsize{0.9cm}\n"
        "\n"
        "\\begin{table}[H]\n"
        "\\centering\n"
        "\\begin{tblr}{\n"
        "  colspec = {X[l,h,\\cellsize]X[l,h,\\cellsize]X[l,h,\\cellsize]X[l,h,\\cellsize]X[l,h,\\cellsize]},\n"
        "  stretch = 0,\n"
        "  rowsep = 2pt,\n"
        "  row{1-5} = {\\cellsize - 4pt, font=\\large\\bfseries},\n"
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
        "\\vspace{0.5cm}\n"
        "\n"
        "\\begin{multicols}{2}\n"
        "    {\\Large Across}\n"
        "    \\begin{enumerate}\n"
        "    \\large\n"
        ""+clue_desc['across']+""
        "    \\end{enumerate}\n"
        "    \n"
        "    \\columnbreak\n"
        "    \n"
        "    {\\Large Down}\n"
        "    \\begin{enumerate}\n"
        "    \\large\n"
        ""+clue_desc['down']+""
        "    \\end{enumerate}\n"
        "\\end{multicols}\n"
        "\n"
        "\\vspace{0.6cm}\n"
        "Created \\today\n"
        "\\end{center}\n"),(
        "\\begin{center}\n"
        "{\n"
        "\\huge{Solution - "+data['title']+"}\n"
        "}\n"
        "\n"
        "\\begin{table}[H]\n"
        "\\centering\n"
        "\\rotatebox[origin=c]{180}{\n"
        "\\begin{tblr}{\n"
        "  colspec = {X[c,m,\\solcellsize]X[c,m,\\solcellsize]X[c,m,\\solcellsize]X[c,m,\\solcellsize]X[c,m,\\solcellsize]},\n"
        "  stretch = 0,\n"
        "  rowsep = 2pt,\n"
        "  row{1-5} = {\\solcellsize - 4pt, font=\\Large\\bfseries},\n"
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
        print("Usage: xw-to-latex.py [-o outfile] infile...")
        sys.exit(1)

    cat_cw = (
        "\\documentclass[a4paper]{article}\n"
        "\\usepackage{graphicx}\n"
        "\n"
        "\\usepackage[table]{xcolor}\n"
        "\\usepackage{tabularray}  \n"
        "\\usepackage{float}\n"
        "\\usepackage{multicol}\n"
        "\n"
        "\\title{Crossword Puzzle}\n"
        "\\author{Author}\n"
        "\\date{\\today}\n"
        "\n"
        "\\begin{document}\n"
        "\\pagenumbering{gobble}\n"
        "\n"
        "\\def\\cellsize{1.5cm}\n"
        "\\def\\solcellsize{0.9cm}\n"
    )
    cat_sol = cat_cw

    outfile = "a"

    i = 1
    while i < len(sys.argv):
        if sys.argv[i][0] == '-':
            if len(sys.argv[i]) == 1:
                print("Error: '-' without 'o'")
                sys.exit(1)
            if sys.argv[i][1] != 'o':
                print("Error: unknown option '-"+sys.argv[i][1]+"'")
                sys.exit(1)

            outfile = sys.argv[i+1]
            i += 2
            continue

        infile = sys.argv[i]
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
            if data['size']['rows'] != N or data['size']['cols'] != M:
                print(
                "Error (invalid input): size is "+str(data['size']['rows'])+"x"+str(data['size']['cols'])+", "
                "expected "+str(N)+"x"+str(M)+" in file "+str(i)+" ("+infile+").")
                sys.exit(1)

            cw, sol = to_latex(data)
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

