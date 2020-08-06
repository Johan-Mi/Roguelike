#!/bin/sh

src_file="$1"

dest_file="gfx/${src_file%%.png}.py"
echo "$(echo ${src_file%%.png} | tr '[:lower:]' '[:upper:]')_TEXTURE = (" \
	> $dest_file
2ff < "gfx/src/$src_file" \
	| hexdump -dv \
	| tail -n+2 \
	| head -n-1 \
	| awk '{print "(" int($2/256) "," int($3/256) "," int($4/256) "),(" \
	int($6/256) "," int($7/256) "," int($8/256) "),"}' \
	>> $dest_file
echo ')' >> $dest_file
