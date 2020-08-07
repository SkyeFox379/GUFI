import sys

#we should only call this script on the average file that holds the averages from each commit

def calculate_difference():
    #looping 8 times because there are 8 stats we are tracking
    for i in range(8):
        result = current_stats[i] - target_stats[i]
        #a negative number for a result means there was an imporvement in performance
        if i%8 == 0:
            result_stats["open directories"] = result
        elif i%8 == 1:
            result_stats["open databases"] = result
        elif i%8 == 2:
            result_stats["descend"] = result
        elif i%8 == 3:
            result_stats["sqlsum"] = result
        elif i%8 == 4:
            result_stats["sqlent"] = result
        elif i%8 == 5:
            result_stats["close databases"] = result
        elif i%8 == 6:
            result_stats["close directories"] = result
        elif i%8 == 7:
            result_stats["real time"] = result



def print_results():
    for key, value in result_stats.items():
        if value > allowed_variance:
            print(key + "\n     " + "Performance regressed by:   " + str(value) + "s\n")
        elif value < -1 * allowed_variance:
            print(key + "\n     " + "Performance improved by:   " + str(-1*value) + "s\n")
        else:
            print(key + "\n     " + "No change in time\n")


#argv[1] is the file containing all the averages we've collected from each commit
#argv[2] is the current commit hash
#argv[3] is the commit hash we want to commpare the latest commit to
averageFile = sys.argv[1]
pristineFile = sys.argv[2]
current_commit = sys.argv[3]
target_commit = sys.argv[4]
allowed_variance = float(sys.argv[5])


current_stats = []
target_stats = []

result_stats = {
    "open directories" : 0,
    "open databases" : 0,
    "descend" : 0,
    "sqlsum" : 0,
    "sqlent" : 0,
    "close databases" : 0,
    "close directories" : 0,
    "real time" : 0
}

#average file should only have our current commit averages
with open(averageFile, 'r') as f:
    lines = f.readlines()

#since the avg file only have one entry, we store every line except the commit hash line
for line in lines:
    if not current_commit in line:
        current_stats.append(float(line))


#we are going to compare against the target hash from the pristine file
with open(pristineFile, 'r') as f:
    lines = f.readlines()

#iterator to tell what line we are on in the pristine file
i = 0

#search the file until we find the target hash
#then we know the 8 lines under the hashes are our stats
for line in lines:
    if target_commit in line:
        for k in range (i, i+8):
            target_stats.append(float(lines[k+1])) #k+1 so we skip the commit hash line
        break
    i+=1


calculate_difference()
print_results()
