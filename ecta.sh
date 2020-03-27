#!/bin/bash

vol=$(($1-1932))

mkdir ecta_$1
cd ecta_$1

rm links.txt

for i in `seq 6`
do
	lynx -dump "https://onlinelibrary.wiley.com/toc/14680262/$1/$vol/$i"| grep doi/pdf | awk '{print $2}' >> links.txt
	sleep 10
done

for f in `sed 's/pdf/pdfdirect/g' links.txt`
do
	wget -nc --user-agent=Mozilla $f
	echo $f
	sleep 5
done
