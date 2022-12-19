rm -f a.out
./build.sh
echo "[GRADER] built binary"
chmod +x test/*.sh
rm -rf test/traces
mkdir test/traces
python3 test/run_tracer.py
echo '[GRADER] ran tracer'
if [ -f test/forked ]; then
    echo "[GRADER] found forked"
fi
if [ ! -f test/functionality.csv ]; then
    echo "[GRADER] functionality.csv not found"
fi
echo '[GRADER] run diff now'

python3 test/diff_traces.py
if [ ! -f test/diff_traces.csv ]; then
    echo "[GRADER] diff_traces.csv not found"
fi
