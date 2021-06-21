#!/bin/bash

mkdir jfqa
cd jfqa

lynx -dump https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/all-issues | grep '/issue/' | awk '{print $2}' > links.txt

rm pdflist.txt

for link in $(cat links.txt)
do
	pdfs=$(lynx -dump $link | rg "pdf$" | awk '{print $2}')
	for pdf in $(echo $pdfs)
	do
		echo $pdf >> pdflist.txt
		echo $pdf
		wget -nc --user-agent=Mozilla $pdf
	sleep 5
	done
done
