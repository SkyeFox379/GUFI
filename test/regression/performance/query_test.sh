set -e

ROOT="$(realpath ${BASH_SOURCE[0]})"
ROOT="$(dirname ${ROOT})"
ROOT="$(dirname ${ROOT})"
ROOT="$(dirname ${ROOT})"
ROOT="$(dirname ${ROOT})"

#location of additional scripts
GUFI_QUERY="${ROOT}/build/src/gufi_query"
PARSE_SCRIPT="${ROOT}/build/test/regression/parse_stats.py"
AVERAGE_SCRIPT="${ROOT}/build/test/regression/averages.py"
COMPARE_SCRIPT="${ROOT}/build/test/regression/history_compare.py"
COMMIT_TO_FILE_SCRIPT="${ROOT}/build/test/regression/pristine_file.py"


#defaults
NUM_OF_THREADS=64
NUM_OF_TIMES=0
VARIANCE=1 #1 second variance default
summary=0
entries=0
compare=0
commit_to_file=0

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
	-n)
	NUM_OF_THREADS="$2"
	shift #shift past -n
	shift #shift past number of threads
	;;

	-v)
	VARIANCE="$2"
	shift #shift past -v
	shift #shift past allowed variance
	;;

	-compare)
	#this is an option because what if this is your first entry and you don't want to compare
	compare=1
	TARGET_COMMIT=$2
	shift #shift past -compare
	shift #shift past commits back
	;;

	-commit)
	#we want to commit to the prestine file
	#if we see this flag, then the script will only call the pristine file script 
	#it won't run the query or averages script
	commit_to_file=1
	shift #shift past -commit
	;;

	-S)
	SUMMARY_QUERY="$2"
	INDEX="$3"
	NUM_OF_TIMES="$4"
	FILE_NAME="$5"
	summary=1
	shift #shift past -S
	shift #shift past summary query
	if [[ "$INDEX" != "-E" ]] #check to see if there's isn't an entries query
	then
		shift #shift past the index
		shift #shift past the number of times to run the query
		shift #shift past the file name
	fi
	;;

	-E)
	ENTRIES_QUERY="$2"
	INDEX="$3"
	NUM_OF_TIMES="$4"
	FILE_NAME="$5"
	entries=1
	shift #shift past -E
	shift #shift past entries query
	if [[ "$INDEX" != "-S" ]] #check to see if there's isn't a summary query
	then
		shift #shift past the index
		shift #shift past the the number of times to run the query
		shift #shift past the file name
	fi
	;;
esac
done

#get commit ID
COMMIT=$(git --git-dir="${ROOT}"/.git rev-parse --short HEAD)
#commit we want to compare to
#TARGET_COMMIT=$(git --git-dir="${ROOT}"/.git rev-parse --short HEAD~"${COMMITS_BACK}")


TMP_FILE=tmp_"$FILE_NAME"

(

COUNTER=0

while [[ "$COUNTER" -lt "$NUM_OF_TIMES" && "$commit_to_file" != 1 ]]; do
	if [[ "${summary}" -eq 1 && "${entries}" -eq 1 ]]
	then
		(bash -c "echo 3 > /proc/sys/vm/drop_caches" && "${GUFI_QUERY}" -n "${NUM_OF_THREADS}" -S "${SUMMARY_QUERY}" -E "${ENTRIES_QUERY}" "${INDEX}" | wc -l) &>> "${TMP_FILE}"

	elif [[ "${summary}" -eq 1 ]]
	then
		(bash -c "echo 3 > /proc/sys/vm/drop_caches" && "${GUFI_QUERY}" -n "${NUM_OF_THREADS}" -S "${SUMMARY_QUERY}" "${INDEX}" | wc -l) &>> "${TMP_FILE}"

	elif [[ "${entries}" -eq 1 ]]
	then
		(bash -c "echo 3 > /proc/sys/vm/drop_caches" && "${GUFI_QUERY}" -n "${NUM_OF_THREADS}" -E "${ENTRIES_QUERY}" "${INDEX}" | wc -l) &>> "${TMP_FILE}"
	fi

	#this script will create/append to history_"$FILE_NAME" file with the parsed entries
	python3 ${PARSE_SCRIPT} "$FILE_NAME" "$TMP_FILE"

	#delete the tmp stats file after the python script takes the information we care about
	rm "$TMP_FILE"

	let COUNTER=COUNTER+1
done

HISTORY_FILE=history_"$FILE_NAME"
AVG_FILE=avg_"$FILE_NAME"
PRISTINE_FILE=pristine_"$FILE_NAME"

#this script will create/overwrite avg"$FILE_NAME" with the average from HISTORY_FILE
#if we run this script saying to commit then we don't need to calculate any averages
if [[ $commit_to_file != 1 ]]
then
	python3 ${AVERAGE_SCRIPT} "$HISTORY_FILE" "$FILE_NAME" "$COMMIT"
	rm "$HISTORY_FILE"
fi

if [[ "$compare" == 1 && "$commit_to_file" != 1 ]]
then
	#this will compare the averages between our current commit (located in the avg file) 
	#and the commit we specified (located in pristine file)
	#prints results to the screen
	python3 ${COMPARE_SCRIPT} "$AVG_FILE" "$PRISTINE_FILE" "$COMMIT" "$TARGET_COMMIT" "$VARIANCE"
	rc=$?
	exit $rc
fi

echo "no regression"

#if commit flag was present, then we store this average for our current commit in the pristine file
if [[ "$commit_to_file" == 1 ]]
then
	python3 ${COMMIT_TO_FILE_SCRIPT} "$AVG_FILE" "$PRISTINE_FILE" "$COMMIT"
fi
)

