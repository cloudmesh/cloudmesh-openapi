import os
import sys
from cloudmesh.common.Shell import Shell
import pandas as pd
import numpy as np
from cloudmesh.common.Benchmark import Benchmark
from timeit import default_timer

def main(argv):
    Benchmark.Start()
    home = os.environ['HOME']
    script_output_dir = f"{home}/.cloudmesh/eigenfaces-svm/vm_script_output/"
    benchmark_output_dir = f"{home}/.cloudmesh/eigenfaces-svm/benchmark_output/"

    if not os.path.exists(f"{home}/.cloudmesh/eigenfaces-svm"):
        os.mkdir(f"{home}/.cloudmesh/eigenfaces-svm")
    if not os.path.exists(script_output_dir):
        os.mkdir(script_output_dir)
    if not os.path.exists(benchmark_output_dir):
        os.mkdir(benchmark_output_dir)

    # Run script to launch VMs and benchmark OpenAPI service if command line arg "run" passed
    if len(argv) > 1 and argv[1]=="run":
        clouds = ['aws', 'google', 'azure']
        runtimes_dic = {'google': [],
                    'aws': [],
                    'azure': []}
        num_trials = 3
        print(f"Running {num_trials} trials for each cloud in {clouds}")
        for cloud in clouds:
            Shell.run(f"cms set cloud={cloud}")
            for i in range(num_trials):
                vm_name = f"{cloud}-{i}"
                print(f"Creating and running test on VM {vm_name}")
                start = default_timer()
                result = Shell.run(f"{home}/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/eigenfaces-svm-full-script {vm_name} > {script_output_dir}{cloud}-{i}")
                end = default_timer()
                print(f"Script on {vm_name} finished in {end - start} seconds")
                runtimes_dic[cloud].append(end-start)
            runtimes = np.asarray(runtimes_dic[cloud])
            print (f"\n{cloud} script run time mean: {runtimes.mean()}")
            print(f"{cloud} script run time min: {runtimes.min()}")
            print(f"{cloud} script run time max: {runtimes.max()}")
            print(f"{cloud} script run time std: {runtimes.std()}\n")

    # Scarpe benchmark output from script outputs
    print(f'Scraping benchmarks from script output at {script_output_dir}')
    script_outputs = os.listdir(script_output_dir)
    for file in script_outputs:
        with open(f"{script_output_dir}{file}",'r') as f:
            b = open(f"{benchmark_output_dir}{file}-benchmark", "w")
            b.write("csv,timer,status,time,sum,start,tag,uname.node,user,uname.system,platform.version\n")
            found_benchmark = False
            for line in f.readlines():
                if line[0:10] == "# csv,test": #some shells return csv info twice once as error "info" and normal output
                    found_benchmark = True
                    b.write(line[2:]) #keep csv,...
            b.close()
            if not found_benchmark:
                print(f"Error on script {script_output_dir}{file}")
                if os.path.exists(f"{benchmark_output_dir}{file}-benchmark"):
                    os.remove(f"{benchmark_output_dir}{file}-benchmark")

    # Read benchmark output and compute statistics
    print(f'Reading benchmarks from benchmark output at {benchmark_output_dir}')
    columns = ["csv","timer","status","time","sum","start","tag","uname.node","user","uname.system","platform.version, cloud"]
    benchmark_df = pd.DataFrame(columns=columns)
    benchmark_outputs = os.listdir(benchmark_output_dir)
    for file in benchmark_outputs:
        cloud = file.split("-")[0]
        df = pd.read_csv(f"{benchmark_output_dir}{file}")
        df['cloud'] = cloud
        if cloud == 'aws':
            df.loc[df['uname.node'].str.startswith("ip"),["uname.node"]] = 'aws' + "-" +file.split("-")[1]
        benchmark_df = pd.concat([benchmark_df, df])


    print("Printing trial statistics:")
    result = ""
    for cloud in benchmark_df['cloud'].unique():
        result += f"{cloud} has {len(benchmark_df.loc[benchmark_df['cloud']==cloud]['uname.node'].unique())} VM samples.\n"
        for timer in benchmark_df['timer'].unique():
            for host in benchmark_df['uname.node'].unique():
                df = benchmark_df.loc[(benchmark_df['cloud'] == cloud) & (benchmark_df['timer'] == timer) & (benchmark_df['uname.node'] == host), ['time']]
                if len(df.values) > 0:
                    mean = df.values.mean()
                    min = df.values.min()
                    max = df.values.max()
                    std = df.values.std()
                    result += f"{cloud} {timer} {host} samples: {len(df.values)}\n"
                    result += f"{cloud} {timer} {host} mean: {mean}\n"
                    result += f"{cloud} {timer} {host} min: {min}\n"
                    result += f"{cloud} {timer} {host} max: {max}\n"
                    result += f"{cloud} {timer} {host} std: {std}\n\n"

    # graph 1: download_data_local
    # graph 2: scikitlearn_train vs opeanpi_scikitlearn_train
    # graph 3: upload_local vs upload_remote,
    # graph 4  predict_local vs predict_remote


    print(result)
    Benchmark.Stop()
    Benchmark.print()
    return

if __name__ == "__main__":
    main(sys.argv)
