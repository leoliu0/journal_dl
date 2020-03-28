#!/bin/bash
mkdir jel
cd jel

rm issues.txt

lynx -dump https://www.aeaweb.org/journals/jel/issues | grep /issues/ | awk '{print $2}' > links.txt

for i in `cat links.txt`
do
	echo $i
	for url in $(lynx -dump $i | grep "articles?" | awk -F'/' '{print "https://pubs.aeaweb.org/doi/pdfplus/10.1257/"$5}')
	do
		echo $url
		wget -nc --user-agent=Mozilla $url
		sleep 5
	done
done
