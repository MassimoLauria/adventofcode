#!/bin/sh

TIME=/usr/bin/time

for f in code[0-9][0-9].go; do
    echo "Build $f" ; go build $f  >|/dev/null
done

# Warmup
for f in code[0-9][0-9]; do
    $TIME -o /dev/null -f "%E %M Kb %F+%R faults" ./$f 2>&1 >|/dev/null
done

for f in code[0-9][0-9]; do
    echo -n "Run $f  " ; $TIME -f "%E %M Kb %F+%R faults" ./$f >|/dev/null
done
