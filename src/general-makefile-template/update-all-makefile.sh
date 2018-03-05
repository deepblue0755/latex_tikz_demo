#!/bin/bash

files=`find ../ -name 'Makefile'`

if [ ! -f ./Makefile ];then
    echo "error: sorry there's no Makefile in current directory!!"
    exit -1
fi

for file in $files
do
    echo "-----------------------------------------------------"
    echo "$file"
    echo "-----------------------------------------------------"

    diff ./Makefile "$file" >> /dev/null
    if [ $? == 0 ];then
        echo "the $file is same with ./general-makefile/Makefile"
        echo " "
        continue;
    else
        cp -fv ./Makefile $file 
        echo " "
    fi
done


echo "all Makefile is update!"
exit 0
