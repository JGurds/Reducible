#  File: Reducible.py

#  Description:

#  Student Name: Jackson Gurdak

#  Student UT EID: jag22934

#  Partner Name: Jack Rickman

#  Partner UT EID: jhr2368

#  Course Name: CS 313E

#  Unique Number: 52235

#  Date Created: 04/04/2021

#  Date Last Modified: 04/04/2021



import sys

# Input: takes as input a positive integer n
# Output: returns True if n is prime and False otherwise
def is_prime ( n ):
  if (n == 1):
    return False
  limit = int (n ** 0.5) + 1
  div = 2
  while (div < limit):
    if (n % div == 0):
      return False
    div += 1
  return True

# Input: takes as input a string in lower case and the size
#        of the hash table 
# Output: returns the index the string will hash into
def hash_word (s, size):
  hash_idx = 0
  for j in range (len(s)):
    letter = ord (s[j]) - 96
    hash_idx = (hash_idx * 26 + letter) % size
  return hash_idx

# Input: takes as input a string in lower case and the constant
#        for double hashing 
# Output: returns the step size for that string 
def step_size (s, const):
    hash_idx = 0
    for j in range (len(s)):
        letter = ord(s[j]) - 96
        hash_idx = (hash_idx * 26 + letter) % const
    size = const - (hash_idx % const)
    return size


# Input: takes as input a string and a hash table 
# Output: no output; the function enters the string in the hash table, 
#         it resolves collisions by double hashing
def insert_word (s, hash_table):
    pos = hash_word(s, len(hash_table))
    if hash_table[pos] != " ":
      new_pos = step_size(s, 13)
      i = 1
      while hash_table[(pos + new_pos * i) % len(hash_table)] != " ":
        i += 1
        hash_table[(pos + new_pos * i) % len(hash_table)] = s
    else:
      hash_table[pos] = s

# Input: takes as input a string and a hash table 
# Output: returns True if the string is in the hash table 
#         and False otherwise
def find_word (s, hash_table):
    pos = hash_word((s, len(hash_table)))
    if hash_table[pos] == s:
        return True

    if hash_table[pos] == " ":
        new_pos = step_size(s, 13)
        i = 1
        while hash_table[(pos + new_pos * i) % len(hash_table)] != " ":
            if hash_table[(pos + new_pos * i) % len(hash_table)] == s:
              return True
            i += 1
    return False


# Input: string s, a hash table, and a hash_memo 
#        recursively finds if the string is reducible
# Output: if the string is reducible it enters it into the hash memo 
#         and returns True and False otherwise
def is_reducible (s, hash_table, hash_memo):
    if find_word(s, hash_memo):
        return s == "a" or s == "i" or s == "o"
    if find_word(s, hash_memo):
        return True
    for child in parent(s, hash_table):
        if is_reducible(child, hash_table, hash_memo):
            insert_word(s, hash_memo)
            return True
    return False

def parent(s, hash_table):
    reducible = []
    for i in range(len(s)):
        child = s[:i] + s[i+1:]
        if find_word(child, hash_table):
            reducible.append(child)
    return reducible


# Input: string_list a list of words
# Output: returns a list of words that have the maximum length
def get_longest_words (string_list):
    longest_word = []
    longest_length = len(string_list[0])
    for i in range(len(string_list)):
        if len(string_list[i]) == longest_length:
            longest_word.append(string_list[i])
        else:
          return longest_word


def main():
  # create an empty word_list
  word_list = []

  # read words from words.txt and append to word_list
  for line in sys.stdin:
      line = line.strip()
      word_list.append (line)

  # find length of word_list
  length = len(word_list)

  # determine prime number N that is greater than twice
  # the length of the word_list
  primeNum = length * 2
  while not is_prime(primeNum):
      primeNum += 1


  # create an empty hash_list
  hash_list = []

  # populate the hash_list with N blank strings
  for i in range(primeNum):
      hash_list.append(" ")

  # hash each word in word_list into hash_list
  # for collisions use double hashing
  for word in word_list:
      insert_word(word, hash_list)

  # create an empty hash_memo of size M
  # we do not know a priori how many words will be reducible
  # let us assume it is 10 percent (fairly safe) of the words
  # then M is a prime number that is slightly greater than 
  # 0.2 * size of word_list
  m = round(length * 0.2)
  while not is_prime(m):
      m +=1

  hash_memo = []


  # populate the hash_memo with M blank strings
  for i in range(m):
    hash_memo.append(" ")



  # create an empty list reducible_words
  reducible_words = []

  # for each word in the word_list recursively determine
  # if it is reducible, if it is, add it to reducible_words
  # as you recursively remove one letter at a time check
  # first if the sub-word exists in the hash_memo. if it does
  # then the word is reducible and you do not have to test
  # any further. add the word to the hash_memo.
  for word in word_list:
      reducible = is_reducible(word, hash_list, hash_memo)
      if reducible:
          reducible_words.append(word)

  # find the largest reducible words in reducible_words
  longest_word = get_longest_words(reducible_words)

  # print the reducible words in alphabetical order
  # one word per line
  longest_word.sort()
  for word in longest_word:
      print(word)

if __name__ == "__main__":
  main()

