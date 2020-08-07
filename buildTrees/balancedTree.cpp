//Takes in max depth and max width as command line arugments

#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

using namespace std;

int max_depth;
int max_width;
int num_files = 3;
int count = 1;

void create_tree(string path, int layer)
{
	//int num_files = rand() % 4;
	if(num_files > 0)
	{	
		ofstream file;
    	for(int f = 0; f < num_files; f++)
		{
        	file.open (path + "/file" + to_string(f));
        	file << "random file\n";
        	file.close();
    	}
	}

	if(layer >= max_depth)
		return;

	for(int i = 0; i < max_width; i++)
	{
		//print out directory count every 10,000 directories
		if(count % 10000 == 0)
			cout << count << endl;
		count ++;
		string tmp_path = path +  "/d" + to_string(i);
		filesystem::create_directories(tmp_path);
		create_tree(tmp_path, layer+1);
	}
}

int main(int argc, char *argv[])
{

	//check to see if user entered arguments
	if(argc < 3)
	{
		cout << "Please enter max depth and max width" << endl;
		exit(1);
	}

	srand(time(NULL));

	max_depth = atoi(argv[1]);
	max_width = atoi(argv[2]);
	
	//create parent directory
	filesystem::create_directories("balancedTallTree");

	create_tree("balancedTallTree", 1);

	count++;
	cout << count << " Directories created" << endl;
	
	return 0;
}
