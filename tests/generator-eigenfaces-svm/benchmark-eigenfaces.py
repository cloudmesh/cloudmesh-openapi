import os
import sys
from cloudmesh.common.Shell import Shell
import pandas as pd
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
        clouds = ['google', 'aws', 'azure']
        num_trials = 2
        print(f"Running {num_trials} trials for each cloud in {clouds}")
        for cloud in clouds:
            Shell.run(f"cms set cloud={cloud}")
            for i in range(num_trials):
                vm_name = f"{cloud}-{i}"
                print(f"Creating and running test on VM {vm_name}")
                start = default_timer()
                result = Shell.run(f"{home}/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/eigenfaces-svm-full-script {vm_name}> {script_output_dir}{cloud}-{i}")
                end = default_timer()
                print(f"Script on {vm_name} finished in {end - start} seconds")

    # Scarpe benchmark output from script outputs
    print(f'Scraping benchmarks from script output at {script_output_dir}')
    script_outputs = os.listdir(script_output_dir)
    for file in script_outputs:
        with open(f"{script_output_dir}{file}",'r') as f:
            b = open(f"{benchmark_output_dir}{file}-benchmark", "w")
            found_benchmark = False
            count = 0
            for line in f.readlines():
                if line[0:6] == "# csv," and count < 5: #some shells return csv info twice once as error "info" and normal output
                    found_benchmark = True
                    count +=1
                    b.write(line[2:]) #keep csv,...
            b.close()
            if not found_benchmark:
                print(f"Error on script {script_output_dir}{file}")
                if os.path.exists(f"{benchmark_output_dir}{file}-benchmark"):
                    os.remove(f"{benchmark_output_dir}{file}-benchmark")

    # Read benchmark output and compute statistics
    print(f'Reading benchmarks from benchmark output at {benchmark_output_dir}')
    columns = ["csv","timer","status","time","sum","start","tag","uname.node","user","uname.system","platform.version"]
    benchmark_df = pd.DataFrame(columns=columns)
    benchmark_outputs = os.listdir(benchmark_output_dir)
    for file in benchmark_outputs:
        df = pd.read_csv(f"{benchmark_output_dir}{file}")
        benchmark_df = pd.concat([benchmark_df, df])



    print("Printing trial statistics:")
    benchmark_df['cloud'] = benchmark_df['uname.node'].str.slice(0,-2)
    benchmark_df.loc[(benchmark_df['cloud'] != 'google') & (benchmark_df['cloud'] != 'azure'),['cloud']] = 'aws' #fix for aws putting IP in uname.node insteads of VM name
    result = ""
    for cloud in benchmark_df['cloud'].unique():
        for timer in benchmark_df['timer'].unique():
            mean = benchmark_df.loc[(benchmark_df['cloud'] == cloud) & (benchmark_df['timer'] == timer),['time']].values.mean()
            min = benchmark_df.loc[(benchmark_df['cloud'] == cloud) & (benchmark_df['timer'] == timer), ['time']].values.min()
            max = benchmark_df.loc[(benchmark_df['cloud'] == cloud) & (benchmark_df['timer'] == timer), ['time']].values.max()
            std = benchmark_df.loc[(benchmark_df['cloud'] == cloud) & (benchmark_df['timer'] == timer), ['time']].values.std()
            result += f"{cloud} {timer} mean: {mean}\n"
            result += f"{cloud} {timer} min: {min}\n"
            result += f"{cloud} {timer} max: {max}\n"
            result += f"{cloud} {timer} std: {std}\n"

    print(result)
    Benchmark.Stop()
    Benchmark.print()
    return
if __name__ == "__main__":
    main(sys.argv)
