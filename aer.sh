#!/bin/bash
mkdir aer
cd aer

rm issues.txt

lynx -dump https://www.aeaweb.org/journals/aer/issues | grep /issues/ | awk '{print $2}' > links.txt

for i in `cat links.txt`
do
	echo $i
	for url in `lynx -dump $i | grep "articles?" | awk '{print $2}' | sed 's/?id=/\/pdf\/doi\//g'`
	do
		echo $url
		wget -nc --user-agent=Mozilla $url
		sleep 5
	done
done
