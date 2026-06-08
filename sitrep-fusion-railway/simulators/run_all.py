import subprocess, sys, time, pathlib

base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
here = pathlib.Path(__file__).parent

scripts = [
    "drone_simulator.py",
    "rf_simulator.py",
    "camera_simulator.py",
    "aircraft_simulator.py",
    "cyber_simulator.py",
]

procs = []
for s in scripts:
    procs.append(subprocess.Popen([sys.executable, str(here / s), base_url]))
    time.sleep(1)

try:
    for p in procs:
        p.wait()
except KeyboardInterrupt:
    for p in procs:
        p.terminate()
