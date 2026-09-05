# Phil-crossword-to-LaTeX

### Overview

Python script to convert .xw crossword files (JSON format) from [Phil](https://www.jmviz.dev/Phil/) to LaTeX for pretty printing.

This utility may receive many .xw files as command line arguments and will concatenate the puzzles together into one big `.tex` as well as concatenate the puzzle solutions into one big `.tex`.

**Important: Only 5x5 (mini) size is currently supported. Changing constants in code is not enough to change this.**

Also note that the output may require somewhat extensive manual adjustment depending on how much text is in your clues. For instance, I manually adjust some of the `\vspace`s and I like to use `multicols` for the solutions.



### Usage

Run: `python3 xw-to-latex.py [-o outfile] infile...`



This program will write two files as output:

* `outfile`-cw.tex

  * Concatenated crossword puzzles, in the order they were given.

* `outfile`-sol.tex

  * Concatenated crossword puzzle solutions, in the order they were given.

    

### Example

`python3 xw-to-latex.py -o example/output example/blank-1.xw example/blank-2.xw`

or

`python3 xw-to-latex.py -o example/output example/blank-*`

This will (re)generate the concatenated puzzles and solutions into  `output-cw.tex` and `output-sol.tex` in the `example/` directory.
