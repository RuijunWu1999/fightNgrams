def LevenshteinDistance_FullMatrix(s,t):
    #// for all i and j, d[i,j] will hold the Levenshtein distance between
    #// the first i characters of s and the first j characters of t
    #declare int d[0..m, 0..n]
    #set each element in d to zero
    m = len(s)
    n = len(t)
    d = [[0 for x in range(n+1)] for x in range(m+1)]

    # // source prefixes can be transformed into empty string by
    # // dropping all characters
    for i in range(m+1):
        d[i][0] = i
        #d[i, 0] := i

    #// target prefixes can be reached from empty source prefix
    #// by inserting every character
    for j in range(n+1):
        d[0][j] = j
        #d[0, j] := j

    for j in range(1,n+1):
        for i in range(1,m+1):
            #// cost of substitution
            if s[i-1] == t[j-1]:
                subCost = 0
            else:
                subCost = 1

            d[i][j] = min(d[i-1][j] + 1, # deletion
                        d[i][j-1] + 1, # insertion
                        d[i-1][j-1] + subCost) # substitution

    return d[m][n]

# From Levenshtein wiki, transitioned from C++ version
def LevenshteinDistance_TwoRows(s,t):
    # Corrected Python3 Version
    #// create two work vectors of integer distances
    m = len(s)
    n = len(t)
    max_m = max(m, n)
    v0 =[x for x in range(max_m+1)]
    v1 =[0 for x in range(max_m+1)]

    for i in range( m ):
        # java, python index starts from 0, and m not included.
        #// calculate v1 (current row distances) from the previous row v0
        #// first element of v1 is A[i + 1][0]
        #// edit distance is last element of v0,
        #// edit distance is delete (i + 1) chars from s to match empty t
        v1[0] = i + 1

        # // use formula to fill in the rest of the row
        for j in range( n ):
            #// calculating costs for A[i + 1][j + 1]
            deletionCost = v0[j + 1] + 1
            insertionCost = v1[j] + 1
            if s[i] == t[j]:
                substitutionCost = v0[j]
            else:
                substitutionCost = v0[j] + 1
            v1[j + 1] = min(deletionCost, insertionCost, substitutionCost)

        #// copy v1 (current row) to v0 (previous row) for next iteration
        #// since data in v1 is always invalidated, a swap without copy could be more efficient
        v0 = v1[:]
    return v0[n]


def main():
    print("throw", "throng",LevenshteinDistance_TwoRows("throw", "throng"))
    print("throough", "through",LevenshteinDistance_TwoRows("throough", "through"))
    print("kitten", "sitting",LevenshteinDistance_TwoRows("kitten", "sitting"))
    print("alice", "alex",LevenshteinDistance_FullMatrix("alice", "alex"))
    return


if __name__ == "__main__":
    main()

