import numpy as np
import subprocess
import json
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
from matplotlib.backends import backend_pdf

def run_traceroute(hostnames, num_packets, output_filename):
    ls_output = subprocess.check_output("traceroute -a -q 5 google.com", shell=True)
    print ls_output
    
    
    
if __name__ == "__main__":
    run_traceroute(1,1,1)