#!/bin/sh

echo "\nChecking coverage for Python code\n"

COV_THRESHOLD=100;
pytest tests.py --cov=yaar --cov-report= ;
ERROR=$?;

COV_REPORT=`coverage report -m`;
coverage=`echo "$COV_REPORT" | grep 'yaar' | sed 's/yaar\.py\s*\w*\s*\w*\s*\w*\s*\w\s*//g' | cut -d'%' -f1`;


echo 'coverage was:' $coverage'%'

if [ "$ERROR" != "0" ]
then
    if [ $coverage -eq $COV_THRESHOLD ]
    then
	echo "But something went wrong";
	exit 1
    else
	echo "And something went wrong"
	exit 1
    fi
fi


if [ $coverage -eq $COV_THRESHOLD ]
then
    echo "Yay! Everything ok!";
    exit 0;
else
    coverage report -m
    exit 1
fi
