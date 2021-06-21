#!/bin/bash

vol=$(($1-1945))

mkdir $1_jf
cd $1_jf

rm links.txt

for i in `seq 6`
do
	echo "https://onlinelibrary.wiley.com/toc/15406261/$1/$vol/$i"
	lynx -dump "https://onlinelibrary.wiley.com/toc/15406261/$1/$vol/$i"| grep doi/epdf | awk '{print $2}' >> links.txt
	sleep 10
done

for f in $(cat links.txt)
do
	wget -nc --user-agent=Mozilla $f
	echo $(basename "$f")
	mv $(basename "$f") $(basename "$f.pdf")
	sleep 5
done
