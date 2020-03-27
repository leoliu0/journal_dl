#!/bin/bash

vol=$(($1-1892))

mkdir jpe_$1
cd jpe_$1

rm links.txt

for i in `seq 6`
do
	lynx -dump https://www.journals.uchicago.edu/toc/jpe/$1/$vol/$i | grep pdfplus | awk '{print $2}' >> links.txt
	sleep 10
done

for f in `cat links.txt`
do
	wget -nc --user-agent=Mozilla $f
	echo $f
	sleep 5
done
