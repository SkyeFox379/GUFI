# creates a random tree based on your specified min depth, max depth, min width, max width

import os, sys
import argparse
import random


random.seed(8675309)

parser = argparse.ArgumentParser()
parser.add_argument("min_depth", help = "specifies the min depth of the tree", type = int)
parser.add_argument("max_depth", help = "specifies the max depth of the tree", type = int)
parser.add_argument("min_width", help = "specifies the min width of the tree", type = int)
parser.add_argument("max_width", help = "specifies the max width of the tree", type = int)
parser.add_argument("-cf", help = "create files of random size in the created tree", action = "store_true")

args = parser.parse_args()

def create_tree(current_dir, layer_num):

    # checks if we reached max depth
    # there is a 1 in 20 chance a directory that has reached min depth becomes a dead end before reaching max depth
    if layer_num > args.min_depth and (random.randrange(0,19) == 0 or layer_num >= args.max_depth):
        # if we specified files, random amount of files are created
        if args.cf:
            num_files = random.randrange(0,10)
            for i in range(num_files):
                with open(os.path.join(current_dir, "myFile" + str(i)), 'wb') as fout:
                    fout.write(os.urandom(random.randrange(1,2048)))
        return


    width = random.randrange(args.min_width, args.max_width)
    for i in range(width):
        tmp_path = os.path.join(current_dir, "dir" + str(layer_num) + "_" + str(i))
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
            # if we specified files, random amount of files are created
            if args.cf:
                num_files = random.randrange(0,10)
                for i in range(num_files):
                    with open(os.path.join(current_dir, "myFile" + str(i)), 'wb') as fout:
                        fout.write(os.urandom(random.randrange(1,2048)))
            create_tree(tmp_path, layer_num + 1)
 
create_tree(os.path.join(".", "randomTree"), 0)
