#!/home/nhatz/Code/Python_3/PY3/bin/python3

import sys
PROMPT = "[xkcd Parser]"

try:
    from splinter import Browser
    import xkcd_helpers
except:
    print (PROMPT + " Missing dependencies.\n\tMake sure:\n\t\txkcd_helper.py exists in ./\n\t\tsplinter is installed")
    exit (1)

EXPLAIN = 'http://www.explainxkcd.com/wiki/index.php/'

status, start, end = xkcd_helpers.getArgs (sys.argv[1:])
if (status == 1): # Success
    print (PROMPT + " Requested fetch: " + str (start) + " to " + str (end))
elif (status == -1): #  
    print (PROMPT + " Invalid or insufficient arguments. Make sure to provide two numbers.")
    exit (2)

try: 
    bruh = Browser ()
except:
    print (PROMPT + " Failed to start the browser.")
    exit (3)

print (PROMPT + " Starting fetch...")

# end + 1 because range() works like that
for i in range(start, end + 1):
    url = EXPLAIN + str (i)
    print (PROMPT + " Fetching: " + url)
    status, transcript, alt = xkcd_helpers.fetch (bruh, url)

    if (status == 1):
        print (PROMPT + " Requested elements retrieved")
        print ("[Transcript]\n" + transcript + "\n[Alt]\n" + alt + "\n[URL]\n" + url)
    elif (status == -1):
        print (PROMPT + " Couldn't retrieve the requested elements in webpage:\n\t[URL]: " + url)
    elif (status == -2):
        print (PROMPT + " Unknown error. Stoping script.")
        bruh.quit ()
        exit (4)
    else:
        print (PROMPT + " Unexpected return code from fetching. Stoping script.")
        bruh.quit ()
        exit (5)

bruh.quit ()

print (PROMPT + " Done.")
