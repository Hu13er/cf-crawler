#!/bin/sh

URL_RATED_LIST='http://codeforces.com/api/user.ratedList?activeOnly=true'
DATA='data.json'
MAIN_DB='maindb.csv'
DATA_CSV='db.csv'
USERS_CSV='users.csv'
CONTEST_LIST='contest.list.json'
URL_CONTEST_LIST='http://codeforces.com/api/contest.list'
DIFF='diff.csv'


echo "Starting..."

if [ ! -e $DATA ]
then
	echo "Downloading main dataset..."
	curl $URL_RATED_LIST > ".tmp.$DATA"

	python -m json.tool < ".tmp.$DATA" > $DATA
	rm ".tmp.$DATA"
	echo 'Done.'
fi

if [ ! -e $DATA_CSV ]
then
	echo 'making $DATA_CSV...'
	python3.5 "csv_maker.py" $DATA --all > $DATA_CSV
	echo "Done."
fi

if [ ! -e $USERS_CSV ]
then
	echo "making $USERS_CSV"
	python3.5 "csv_maker.py" $DATA --handle > $USERS_CSV
	echo "Done."
fi

echo "Building user_download.go..."
go build "user_download.go"
if [ $? != 0 ]
then
	echo "Can not compile user_download.go"
	exit
fi
echo "Running user_download.go"
mkdir -p user_info
mkdir -p user_rating
mkdir -p user_submition
touch readed.csv
export MACHINE_COUNT=2
./user_download $USERS_CSV

if [ ! -e $CONTEST_LIST ]
then
	echo 'Downloading Contest List...'
	curl $URL_CONTEST_LIST > $CONTEST_LIST
	echo 'Done.'
fi

if [ ! -e $MAIN_DB ]
then
	echo 'Making Main db...'
	python3.5 'main_flatter.py'
	echo 'Done.'
fi

mkdir -p rated_submition
rm rated_submition/* &2> /dev/null
echo 'making items in rated_submition...'
python3.5 'contest_flatter.py'
echo 'Done.'

python3.5 'diff_matrix.py' > $DIFF
echo '$DIFF created...'

echo "Done. . ."
