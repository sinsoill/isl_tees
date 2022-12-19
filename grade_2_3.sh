NO_TESTS=5
TIME=30
FILE_NAME=submit_2_2.py
TASK_FOLDER="/home/isl/t2_2"
OP_FOLDER="/home/isl/t2_2/output"
SAMPLES_FOLDER="/home/isl/t2_2/samples"

rm -f oput_*

for ((i = 1; i <= $NO_TESTS; i++)); do
    rm -f $TASK_FOLDER/password.txt
    cp ./samples/$i/password.txt $TASK_FOLDER
    timeout $TIME python3 $TASK_FOLDER/$FILE_NAME $i
    COUNT=1
    OP=$OP_FOLDER/oput_$i
    if [ ! -f $OP ]; then
        echo "[GRADER] Testcase $i : Output file '$OP' not created on first execution: running the script again "
        timeout $TIME python3 $TASK_FOLDER/$FILE_NAME $i
        COUNT=2
        if [ ! -f $OP ]; then
            echo "[GRADER] Testcase $i: Output file not created on second execution: running the script again "
            timeout $TIME python3 $TASK_FOLDER/$FILE_NAME $i
            COUNT=3
            if [ ! -f $OP ]; then
                echo "[GRADER] Testcase $i : Output file not created on third execution: stopping now "
                echo "[GRADER] Failed for: " $i
                STR="failed"
            fi
        fi
    fi
    echo $i,$COUNT,$STR >>executions.txt
done
