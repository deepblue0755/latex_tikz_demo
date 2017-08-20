#!/bin/bash

if [ $# = 1 ]; then
    echo "try to find folder that don't contain pdf file"
    for folder in * 
    do
        if [ -d "$folder" ];then
            cd $folder
            file="${folder%%.pdf}.pdf"
            if [ ! -f $file ]; then
                echo "no pdf files $file  found in $folder"
            fi
            cd ../
        fi
    done
    exit 0
fi

for folder in * 
do
    if [ -d "$folder" ]; then
        cd "$folder"
        if [ ! -f  "Makefile" ]; then
            echo "$folder do not contain Makefile"
            cp -iv ../smart-diagram/Makefile ./
            make 
        fi
        cd ../
    fi
done

