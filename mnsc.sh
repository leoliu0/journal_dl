#!/bin/bash

vol=$(($1-1954))

mkdir $1_mnsc
cd $1_mnsc

rm links.txt

for i in `seq 12`
do
	lynx -dump "https://pubsonline.informs.org/toc/mnsc/$vol/$i"| awk '/doi.org/ {print $2}' | cut -d '/' -f4- | awk '{print "https://pubsonline.informs.org/doi/pdf/"$1}' | grep mnsc >> links.txt
	sleep 1
done

for f in `cat links.txt`
do
	wget -nc --user-agent=Mozilla $f
	echo $f
	sleep 1
done
