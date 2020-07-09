# Tall tree that is only 2 wide
 
import os, sys
import argparse
import random
 
random.seed(8675309)

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


    if layer_num == 0:
        width = 2
        for i in range(width):
            tmp_path = os.path.join(current_dir, "d" + str(layer_num) + "_" + str(i))
            if not os.path.exists(tmp_path):
                os.makedirs(tmp_path)
                # if we specified files, random amount of files are created
                if args.cf:
                    num_files = random.randrange(0,10)
                    for i in range(num_files):
                        with open(os.path.join(current_dir, "myFile" + str(i)), 'wb') as fout:
                            fout.write(os.urandom(random.randrange(1,2048)))
                create_tree(tmp_path, layer_num + 1)

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
            create_tree(tmp_path, layer_num + 1)

create_tree(os.path.join(".", "2_wide_tall_tree"), 0)
