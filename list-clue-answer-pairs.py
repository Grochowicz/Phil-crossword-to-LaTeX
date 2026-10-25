import simplejson as json
import sys
import os

BLANK_CLUE = "(blank clue)"

def add_words(data):
    ret = ""
    N = data['size']['rows']
    M = data['size']['cols']

#   Helper functions and lists
    def valid(i,j):
        return i>=0 and i<N and j>=0 and j<M and data['grid'][M*i+j]!='.'
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

    def get_ans(i,j,direction):
        ret = ""
        if direction == 'across':
            x = 0
            while j+x < M:
                if not valid(i,j+x):
                    break
                ret += data['grid'][M*i+(j+x)]
                x += 1
        else:
            x = 0
            while i+x < N:
                if not valid(i+x,j):
                    break
                ret += data['grid'][M*(i+x)+j]
                x += 1
        return ret

    clues_by_number = {
            'across':[],
            'down':[],
    }
    for direction in ['across','down']:
        for entry in data['clues'][direction]:
            number, _, clue = entry.partition('. ')
            number = int(number)
            clues_by_number[direction].append([number,clue])
    def get_clue(clue_id,direction):
        for [number,clue] in clues_by_number[direction]:
            if number == clue_id:
                return clue
 
    def check_clue(clue_id,direction):
        for [number,clue] in clues_by_number[direction]:
            if number == clue_id:
                return True
        return False
    def is_clue(i,j,clue_id):
        return valid(i,j) and ((not valid(i-1,j) and check_clue(clue_id,'down')) or (not valid(i,j-1) and check_clue(clue_id,'across')))
    def is_clue_dir(i,j,clue_id,direction):
        if direction == 'across':
            return valid(i,j) and (not valid(i,j-1) and check_clue(clue_id,'across'))
        else:
            return valid(i,j) and (not valid(i-1,j) and check_clue(clue_id,'down'))

    clue_cnt = 0
    for i in range(N):
        for j in range(M):
            if is_clue(i,j,clue_cnt+1):
                clue_cnt += 1

#               Filter clues with size less than 3
                for direction in ['across','down']:
                    if is_clue_dir(i,j,clue_cnt,direction):
                        a = get_ans(i,j,direction)
                        b = get_clue(clue_cnt,direction)
                        if b != BLANK_CLUE:
                            #if size_at_least_min(i,j,direction):
                            ret += a+": "+b+"\n"
    return ret

def main():
    if len(sys.argv) < 2:
        print("Usage: "+sys.argv[0]+" infile...")
        sys.exit(1)

    ans = ""

    i = 1
    while i < len(sys.argv):
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

            ans += add_words(data)
        i += 1
    print(ans,end="")

if __name__ == "__main__":
    main()
