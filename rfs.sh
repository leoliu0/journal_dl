#!/bin/bash

year=$(($1-1987))
mkdir rfs_$1
cd rfs_$1

rm issues.txt

for i in `seq 12`
do
	lynx -dump "https://academic.oup.com/rfs/issue/$year/$i" -useragent=Mozilla | grep doi.org | awk '{print $2}' | uniq | grep '.' >> issues.txt
cat issues.txt
sleep 10
done

for i in `cat issues.txt`
do
	url=`lynx -dump $i | grep article-pdf | awk '{print $2}'`
	echo $url
	wget -nc --user-agent=Mozilla $url --wait=20 --waitretry=5 --random-wait
	sleep 5
done
