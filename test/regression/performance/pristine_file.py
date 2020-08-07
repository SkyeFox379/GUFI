import sys
import os

#store averages from this commit into the pristine file
#if there already exists an entry from this commit hash, overwrite it

avgFile = sys.argv[1]
pristineFile = sys.argv[2]
current_commit = sys.argv[3]
tmp_file = "tmp"

#found let's us know if we found an old entry from our current commit hash
found = 0

#creates the file if it does not exists
f = open(pristineFile, 'a')
f.close()

#read in our prestine file so we can search for an entry of our current commit
with open(pristineFile, 'r') as f:
    lines = f.readlines()

#if we find an entry from our current commit, don't put that entry in the tmp file
with open(tmp_file, 'w') as f:
    for line in lines:
        if current_commit in line:
            found = 1
            continue #continue skips one line (can't skip multiple lines so see next line)

        #this line is here so we can skip over the old entry
        elif found > 0 and found < 10: #we do 10 so it eats the blank line at the end
            found+=1
            continue
        else:
            f.write(line)

#if found isn't 0 then we found an entry from our current commit and made a tmp file 
#we need to make the tmp file our new pristine file
if found != 0:
    os.remove(pristineFile)
    os.rename(tmp_file, pristineFile)
else:
    os.remove(tmp_file)


#read in our current commit's averages
with open(avgFile, 'r') as f:
    lines = f.readlines()

#append our current commit's averages to the pristine file
with open(pristineFile, 'a') as f:
    for line in lines:
        f.write(line)

f = open(pristineFile, 'a')
f.write("\n")
f.close()
