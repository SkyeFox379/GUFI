# Tall tree that is only 2 wide
 
import os, sys
import argparse
import random
 
random.seed(8675309)
sys.setrecursionlimit(1000000)

parser = argparse.ArgumentParser()
parser.add_argument("max_depth", help = "specifies the max depth of the tree", type = int)
parser.add_argument("-cf", help = "create files of random size in the created tree", action = "store_true")
 
args = parser.parse_args()
 
def create_tree(current_dir, layer_num):
    # checks if we reached max depth
    if layer_num >= args.max_depth:
        # if we specified files, random amount of files are created
        if args.cf:
            num_files = random.randrange(0,10)
            for i in range(num_files):
                with open(os.path.join(current_dir, "myFile" + str(i)), 'wb') as fout:
                    fout.write(os.urandom(random.randrange(1,2048)))
        return      

    #this makes it so the width is 2 all the way down the tree
    if layer_num == 0:
        width = 2
        for i in range(width):
            if i == 0:
                ans = "left"
            else:
                ans = "right"
            tmp_path = os.path.join(current_dir, ans)
            if not os.path.exists(tmp_path):
                os.makedirs(tmp_path)
                # if we specified files, random amount of files are created
                if args.cf:
                    num_files = random.randrange(0,10)
                    for i in range(num_files):
                        with open(os.path.join(current_dir, "myFile" + str(i)), 'wb') as fout:
                            fout.write(os.urandom(random.randrange(1,2048)))
                os.chdir(tmp_path)
                current_dir = "."
                create_tree(".", layer_num + 1)
                os.chdir("..")

    else:
        tmp_path = os.path.join(current_dir, "d" + str(layer_num))
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
            # if we specified files, random amount of files are created
            if args.cf:
                num_files = random.randrange(0,10)
                for i in range(num_files):
                    with open(os.path.join(current_dir, "myFile" + str(i)), 'wb') as fout:
                        fout.write(os.urandom(random.randrange(1,2048)))
            os.chdir(tmp_path)
            create_tree(".", layer_num + 1)
            os.chdir("..")

create_tree(os.path.join(".", "2_wide_tall_tree"), 0)
