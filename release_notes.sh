#! /bin/bash
echo 'Lets start'
echo 'Details' > unparsed_logs.txt
git log >> unparsed_logs.txt
python ../release_notes_pipeline.py 
 
