"""
Bible search program from public domain KJV text
Can search for words/phrases
Can enter book, chapter, verse
author: james@rubysash.com  08/07/2020

original data file was from: http://www.bibleprotector.com/TEXT-PCE.zip
If that exact data file isn't available, then this program won't work
because it does regex matching.

dumping as json probably not needed.  I was testing different ways to 
parse the data and needed to verify the structure, but if original data
isn't available I'll have to provide json data.

Interface is clunky.   I plan to tkinter it.

Version History
1.0 basic search for bcv only
1.1 added key word searches, word wrapping
1.2 colorized it, jesus said in red (if it matches regex pattern)
1.3 small bugs, formatting, documentation, status, standardized colors
1.4 search by entire chapter, not just verse, removed json dump, added exit
1.5 added more color tags for Jesus Sai|loo|beg|ask|pre|beh but found nentire chapters missing

"""
version = '1.5'

import re           # the main search function
import textwrap     # wrapping text
import codecs       # to avoid utf-8 errors
import sys           # for sys.exit and argv
#import json         # dumping to json

# and the pretty text
from colorama import init
from colorama import Fore, Back, Style
init()

# files in and out
bibledata = 'biblesearch.txt' # in
#biblejson = 'biblesearch.json'  # out


quickhelp = """

Examples:  

Re,22,3 (to display just a verse Revelations 22:3)
Re,22   (to display an entire chapter Revelations 22)

Q       quits
W       will toggle word wrap from 60 characters to none or back
S       will search for any string (case insensitive, otherwise exact)
?       prints this help message, lists the book names

"""

# in case you forgot the abbrevs of the books
books = """
-------------------------------------------
        Book    #       Chapters
-------------------------------------------
        Ge      1       (50)
        Ex      2       (40)
        Le      3       (27)
        Nu      4       (36)
        De      5       (34)
        Jos     6       (24)
        Jg      7       (21)
        Ru      8       (4)
        1Sa     9       (31)
        2Sa     10      (24)
        1Ki     11      (22)
        2Ki     12      (25)
        1Ch     13      (29)
        2Ch     14      (36)
        Ezr     15      (10)
        Ne      16      (13)
        Es      17      (10)
        Job     18      (42)
        Ps      19      (150)
        Pr      20      (31)
        Ec      21      (12)
        Song    22      (8)
        Isa     23      (66)
        Jer     24      (52)
        La      25      (5)
        Eze     26      (48)
        Da      27      (12)
        Ho      28      (14)
        Joe     29      (3)
        Am      30      (9)
        Ob      31      (1)
        Jon     32      (4)
        Mic     33      (7)
        Na      34      (3)
        Hab     35      (3)
        Zep     36      (3)
        Hag     37      (2)
        Zec     38      (14)
        Mal     39      (4)
        Mt      40      (28)
        Mr      41      (16)
        Lu      42      (24)
        Joh     43      (21)
        Ac      44      (28)
        Ro      45      (16)
        1Co     46      (16)
        2Co     47      (13)
        Ga      48      (6)
        Eph     49      (6)
        Php     50      (4)
        Col     51      (4)
        1Th     52      (5)
        2Th     53      (3)
        1Ti     54      (6)
        2Ti     55      (4)
        Tit     56      (3)
        Phm     57      (1)
        Heb     58      (13)
        Jas     59      (5)
        1Pe     60      (5)
        2Pe     61      (3)
        1Jo     62      (5)
        2Jo     63      (1)
        3Jo     64      (1)
        Jude    65      (1)
        Re      66      (22)
"""


# create dictionary to hold bible data from text file
# maybe dumping as json would be better?
bible_dict=dict()

# by default we wrap words at 50
wrapped = 1


def search_bible(values, search_for):
    """
    searches through our dictionary values for string
    builds list of bcv to print later
    """
    keys_list = []
    items_list = values.items()
    searched = re.compile(search_for, re.IGNORECASE)
    for item in items_list:
        if searched.search(item[1]):
            keys_list.append(item[0])
    return keys_list


def search_books(values, search_for):
    # the full list of all books
    # add a : to it so it's james 1:* not James 1* (matches James 11)
    final = search_for + ":"
    keys_list = list(values.keys())

    # built our wanted list
    wanted = [i for i in keys_list if final in i]
    return wanted


def print_verse(bcv):
    """
    prints a bible verse based on book, chapter, verse
    if wrapped flag is set, it wraps text
    """
    print(Style.RESET_ALL,end="")

    # https://pypi.org/project/colorama/ just doing red for stuff Jesus said
    # could be all sorts of colors for all sorts of tpics though if desired
    # my "red Jesus stuff" misses out entire chapters because it doesn't match these things
    # fixme: consider database of verses that match instead of regex
    if re.search("JESUS SAI",bible_dict[bcv], re.IGNORECASE): #108 verses
        print(Fore.RED,end="")
    elif re.search("JESUS ASK",bible_dict[bcv], re.IGNORECASE): # 2 verses
        print(Fore.RED,end="")
    elif re.search("JESUS LOOK",bible_dict[bcv], re.IGNORECASE):
        print(Fore.RED,end="")
    elif re.search("JESUS BEH",bible_dict[bcv], re.IGNORECASE):
        print(Fore.RED,end="")
    elif re.search("JESUS BEG",bible_dict[bcv], re.IGNORECASE):
        print(Fore.RED,end="")
    elif re.search("JESUS PRE",bible_dict[bcv], re.IGNORECASE):
        print(Fore.RED,end="")
    elif re.search("THIS IS MY BODY",bible_dict[bcv], re.IGNORECASE):
        print(Fore.RED,end="")
    #elif re.search("JESUS TOOK BREAD",bible_dict[bcv], re.IGNORECASE):
    #    print(Fore.RED,end="")
    else:
        print(Style.DIM,end="")

    if wrapped:
        # do we want it wrapped at 60 characters?
        wrapper = textwrap.TextWrapper(width=60)
        word_list = wrapper.wrap(text=bible_dict[bcv])
        print(bcv)
        for element in word_list:
            print(element)
        print("\n")
    
    else:
        # if not, then ok, just print it
        print(bcv)
        print(bible_dict[bcv])
        print("\n")

    print(Style.RESET_ALL,end="")


# colorize the status
print(Style.DIM,end="")
print(sys.argv[0] + " version: " + str(version))

# open and read entire file in (31,103 lines)
print("indexing...",end="")
with codecs.open(bibledata, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        # split the line by spaces
        fields=re.split('\s', line)
        
        # first field is the book (Ge)
        book=fields[0]

        # next filed is the chapter:verse, so split it again (1:1)
        cv=re.split(':',fields[1])
        chapter=cv[0]
        verse=cv[1]
        
        # then we want the rest of the block into a text
        text=' '.join(fields[2:])

        # build key, then add to dictionary
        key = book + ' ' + chapter + ':' +verse
        bible_dict[key] = text
print("done")

"""
dump data to json format to verify structure
Not required, just wanted to see the structure
fixme: use json data instead of munging line by line
chiken and egg - already wrote line munger
"""
#print("Dumping to json...",end="")
#with open (biblejson, 'w') as outfile:
#    json.dump(bible_dict, outfile, indent=2)
#print("done: ",biblejson)


# reset colorized
print(Style.RESET_ALL,end="")
print(quickhelp)
print(Style.RESET_ALL,end="")

while True:
    """
    loop over our commands and do stuff:
    W: toggle wrapp
    Q: quit
    S: Search
    ?: prints list of books and help message
    BCV: prints that vers
    """

    print(Fore.GREEN)
    search=input("COMMAND: ")
    print(Style.RESET_ALL,end="")

    if (re.findall(',',search)):

        # figure out if you want B,C or B,C,V
        search_params = search.split(",")
        
        if (len(search_params) == 2):
            # looking for a book, chapter
            book,chapter=map(str.strip,search.split(","))
            key=(book + ' ' + chapter)
            
            # get a list of verses that match our final string
            keys_list = search_books(bible_dict, key)

            if(len(keys_list)<1):
                print("No such Book, Chapter was found: ", key)
                print("\n")
            else:
                # iterate over them and print
                for bcv in keys_list:
                    print_verse(bcv)

        elif (len(search_params) == 3):
            # looking for a book, chapter verse
            # looks like you entered bcv format, or this is default at least
            # fixme: if they don't enter a proper b,c,v it dies, do a re or 
            # otherwise look for 2 commands
            book,chapter,verse=map(str.strip,search.split(","))

            # rebuild it the way our database key stores it
            key=(book + ' ' + chapter + ':' + verse)

            # now go ahead and search
            if(key in bible_dict):
                # key exists, so wrap it to 60 characters with natural breaks
                print_verse(key)
            else:
                # key doesn't exist, remind them 
                print("No such Book, Chapter, Verse was found: ", key)
        else:
            print("Invalid Command.  Enter ? for help")
    else:
        if search=="Q" or search=='q': 
            break
        elif search=="?":
            # I can't remember the book names either...
            print(books)
            print(quickhelp)
        elif search=="W" or search=="w":
            # swap
            wrapped = not wrapped
            print("Wrap mode has now swapped")
        elif search=='S' or search=='s':
            # type cast input into list, then we'll force to string
            keyword = list(map(str,input("Search for: ").split()))
            
            # convert 1 or more words to string
            final = ' '.join(keyword)

            # get a list of verses that match our final string
            keys_list = search_bible(bible_dict, final)

            # iterate over them and print
            for bcv in keys_list:
                print_verse(bcv)

            # done
            if(len(keys_list)<1):
                print("Nothing matched your search: '" + final + "'")
            else:
                print(str(len(keys_list)) + " verses were found in search: '" + final + "'" )
        else:
            print("Invalid Command.  Enter ? for help")



# cleanup
sys.exit()

# sample data from #http://www.bibleprotector.com/TEXT-PCE.zip
"""
Ge 1:1 In the beginning God created the heaven and the earth.
Ge 1:2 And the earth was without form, and void; and darkness [was] upon the face of the deep. And the Spirit of God moved upon the face of the waters.
Ge 1:3 And God said, Let there be light: and there was light.
Ge 1:4 And God saw the light, that [it was] good: and God divided the light from the darkness.
Ge 1:5 And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day.
Ge 1:6 And God said, Let there be a firmament in the midst of the waters, and let it divide the waters from the waters.
Ge 1:7 And God made the firmament, and divided the waters which [were] under the firmament from the waters which [were] above the firmament: and it was so.
Ge 1:8 And God called the firmament Heaven. And the evening and the morning were the second day.
Ge 1:9 And God said, Let the waters under the heave

"""