#!/bin/bash

year=$(($1-1885))
mkdir qje_$1
cd qje_$1

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
	wget -nc --user-agent=Mozilla $url
	sleep 10
done
