#!/usr/bin/python

#==============================================================================#
# DEPENDENCIES LOADING                                                         #
#==============================================================================#
import sys
sys.path.insert (0, '/home/nhatz/Code/GitHub/randi/python/lib')
PROMPT = "[xkcd Parser]"
PREPATH = '/home/nhatz/Code/GitHub/randi/'
EXPLAIN = 'http://www.explainxkcd.com/wiki/index.php/'

REFS = PREPATH + 'json/xkcd.references.json'
COMMON = PREPATH + 'json/xkcd.common.json'

LINK = 'www.explainxkcd.com'

try:
    print (PROMPT + " Loading dependencies.")
    from splinter import Browser
    import json
    import xkcd_helpers
    print (PROMPT + " Dependencies loaded.")
except:
    print (PROMPT + " Missing or broke dependencies.\n \
            \tMake sure:\n \
                    \t\txkcd_helper.py exists in ./\n \
                    \t\tsplinter is installed")
    exit (1)

#==============================================================================#
# FILE LOADING                                                                 #
#==============================================================================#

black_list = list ()
try:
    print (PROMPT + " Loading black list")
    with open (COMMON) as infile:
        black_list = json.load (infile)
    print (PROMPT + " Blacklist loaded.")
except:
    xkcd_helpers.fileNotFound (PROMPT, COMMON)

comic = dict ()
try:
    print (PROMPT + " Loading comics' references")
    with open (REFS) as infile:
        comic = json.load (infile)
    print (PROMPT + " Comics' references loaded")
except:
    xkcd_helpers.fileNotFound (PROMPT, REFS)

#==============================================================================#
# ARGUMENT CHECK                                                               #
#==============================================================================#

args = xkcd_helpers.getArgs (sys.argv [1:])
if (args [0] == 0): # Success
    print (PROMPT + \
            " Requested fetch: " + str (args [1])  + " to " + str (args [2]))
elif (args [0] == -1): #  
    print (PROMPT + \
            " Insufficient arguments. Provide one or two numbers.")
    exit (2)
elif (args [0] == -2):
    print (PROMPT + \
            " Invalid arguments. Provide numbers.")
    exit (3)
else:
    print (PROMPT + \
            " Unexpected return code from args retrieving. Stoping script.")
    exit (6)

#==============================================================================#
# FETCHING                                                                     #
#==============================================================================#

try:
    print (PROMPT + " Opening browser")
    bruh = Browser ()
    print (PROMPT + " Browser opened.")
except:
    print (PROMPT + " Failed to start the browser.")
    exit (4)

print (PROMPT + " Starting fetch...")

# last + 1 because we need to access the last element
for i in range(args [1], args [2] + 1):
    url = EXPLAIN + str (i)
    print (PROMPT + " Fetching: " + url)
    fetch = xkcd_helpers.fetch (bruh, url)
    if (fetch [0] == 0):
        print (PROMPT + " Requested elements retrieved")
        print (PROMPT + " Indexing comic #" + str (i) )
        
        comic[i] = {\
                "number": i, \
                "url": "wwww.xkcd.com/" + str (i), \
                "title": fetch [1], \
                "alt": fetch [2], \
                "transcript": fetch [3], \
                "url": LINK + fetch[4] \
                }
        print (PROMPT + " Comic " + str(i) + " succesfully referenced.")

        # Uncomment for debugging
        # print (comic)
    
    elif (fetch[0] == -1):
        print (PROMPT + \
                " Couldn't retrieve the requested elements in webpage:\n \
                \t[URL]: " + url)
    
    elif (fetch[0] == -2):
        print (PROMPT + " Unknown error. Stoping script.")
        bruh.quit ()
        exit (5)
    
    else:
        print (PROMPT + \
                " Unexpected return code from fetching. Stoping script.")
        bruh.quit ()
        exit (6)

bruh.quit ()

#==============================================================================#
# FILES SAVING                                                                 #
#==============================================================================#

try:
    print (PROMPT + " Saving comic references in " + REFS)
    with open (REFS, 'w') as outfile:
        json.dump (comic, outfile, indent = 4)
    print (PROMPT + " Comic references succesfully saved.")
except:
    print (PROMPT + " Something went wrong while saving the comic file. \
            \n\tThat's not to bad.")

#==============================================================================#
print (PROMPT + " Done.")
#==============================================================================#
