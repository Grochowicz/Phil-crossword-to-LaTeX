# Phil-crossword-to-LaTeX

### Overview - `xw-to-latex.py`

Python script to convert `.xw` crossword files (JSON format) from [Phil](https://www.jmviz.dev/Phil/) to LaTeX for pretty printing.

This utility may receive many .xw files as command line arguments and will concatenate the puzzles together into one big `.tex` as well as concatenate the puzzle solutions into one big `.tex`.

Note that grid sizes different to 5x5 may require adjustment of cell size constants.

Also note that the output may also require somewhat extensive manual adjustment depending on how much text is in your clues. For instance, I manually adjust some of the `\vspace`s and I like to use `multicols` for the solutions.

### Usage

Run: `python3 xw-to-latex.py [-o outfile] [-p] infile...`

* `-o` will specify output file

* `-p` will set language to Portuguese

This program will write two files as output:

* `outfile`-cw.tex

  * Concatenated crossword puzzles, in the order they were given.

* `outfile`-sol.tex

  * Concatenated crossword puzzle solutions, in the order they were given.

### Example

`python3 xw-to-latex.py -o example/output example/blank-1.xw example/blank-2.xw`

or

`python3 xw-to-latex.py -o example/output example/blank-*.xw`

This will (re)generate the concatenated puzzles and solutions into  `output-cw.tex` and `output-sol.tex` in the `example/` directory.

---

### Additional script - `list-clue-answer-pairs.py`

Simple Python utility I use for keeping track of my own clue-writing history. I can manually search for duplicate or similar clues or answers in an aggregate list that includes content extracted from all `.xw` files passed to it.

### Usage

Run: `python3 list-clue-answer-pairs.py infile...`

This program will write an aggregate list of ANSWER: CLUE pairs to `stdout` in the order they appear in the input files.

### Example

`python3 list-clue-answer-pairs.py example/blank-*.xw`

This prints words in the order they come, in the order the files come were passed in, to `stdout`. I would recommend running something along the lines of

`python3 list-clue-answer-pairs.py example/blank-*.xw | sort > example/clue-answer-pairs.txt`
