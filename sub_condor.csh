#!/bin/tcsh

source /afs/cern.ch/work/a/antoniov/env/uproot4/bin/activate.csh

set file=$1
set label=$2
set option1="$3"
set option2="$4"
set option3="$5"
set option4="$6"
set option5="$7"
set option6="$8"
set EXEC=/eos/home-a/antoniov/SWAN_projects/pps-dilepton-analysis
set OUTPUT=/eos/home-a/antoniov/SWAN_projects/pps-dilepton-analysis/output
echo "file: "$file
echo "label: "$label
echo "option: "$option1
echo "option: "$option2
echo "option: "$option3
echo "option: "$option4
echo "option: "$option5
echo "option: "$option6
echo $EXEC
echo $OUTPUT

if ( ! $?PYTHONPATH ) then
    setenv PYTHONPATH ${EXEC}
else
    setenv PYTHONPATH ${PYTHONPATH}:${EXEC}
endif
echo PYTHONPATH set to $PYTHONPATH 
env

echo $PWD

echo 'Running...'
echo python $EXEC/create_table.py --files=$file --label=$label $option1 $option2 $option3 $option4 $option5 $option6
python $EXEC/create_table.py --files=$file --label=$label $option1 $option2 $option3 $option4 $option5 $option6
cp *.h5 $OUTPUT
