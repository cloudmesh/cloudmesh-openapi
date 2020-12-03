import os
import sys
from cloudmesh.common.Shell import Shell
import pandas as pd
import numpy as np
from cloudmesh.common.Benchmark import Benchmark
from timeit import default_timer
from socket import gethostname
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerTuple
from multiprocessing import Pool
from cloudmesh.common.util import HEADING
import requests
from cloudmesh.configuration.Config import Config
import shutil

def test_download_data(ip):
    Benchmark.Start()
    r = requests.get(f"http://{ip}:8080/cloudmesh/EigenfacesSVM/download_data")
    Benchmark.Stop()
    assert r.status_code == 200


def test_train(ip):
    Benchmark.Start()
    r = requests.get(f"http://{ip}:8080/cloudmesh/EigenfacesSVM/train")
    Benchmark.Stop()
    assert r.status_code == 200


def test_upload(ip,cloud):

    url = f"http://{ip}:8080/cloudmesh/upload"
    home = os.environ.get('HOME')
    image_src = f'{home}/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/example_image.jpg'
    Benchmark.Start()
    for i in range(30):
        image_dst = f'{home}/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/example_image{cloud}{i}.jpg'
        shutil.copyfile(image_src,image_dst)
        upload = {'upload': open(image_dst, 'rb')}
        r = requests.post(url, files=upload)
        assert r.status_code == 200
        os.remove(image_dst)
    Benchmark.Stop()


def test_predict(ip, cloud):
    url = f"http://{ip}:8080/cloudmesh/EigenfacesSVM/predict"
    config = Config()
    if cloud == "aws":
        user = config[f"cloudmesh.cloud.aws.default.username"]
        home = f"/home/{user}"
    elif cloud == "azure":
        user = config[f"cloudmesh.cloud.azure.default.AZURE_VM_USER"]
        home = f"/home/{user}"
    elif cloud == "google":
        user = config[f"cloudmesh.profile.user"]
        home = f"/home/{user}"
    Benchmark.Start()
    for i in range(30):
        payload = {'image_file_paths': f'{home}/.cloudmesh/upload-file/example_image{cloud}{i}.jpg'}
        r = requests.get(url, params=payload)
        assert r.status_code == 200
    Benchmark.Stop()

def test_ai_workflow(arg):
    ip, cloud, i = arg
    vm_name=f"{cloud}-{i}"
    home = os.environ['HOME']
    script_output_dir = f"{home}/.cloudmesh/eigenfaces-svm/vm_script_output_multi/"

    if not os.path.exists(f"{home}/.cloudmesh/eigenfaces-svm"):
        os.mkdir(f"{home}/.cloudmesh/eigenfaces-svm")
    if not os.path.exists(script_output_dir):
        os.mkdir(script_output_dir)

    output_file = open(f"{script_output_dir}{vm_name}", 'a')
    old_stdout = sys.stdout
    sys.stdout = output_file
    for i in range(30):
        test_download_data(ip)
        test_train(ip)
        test_upload(ip,cloud)
        test_predict(ip,cloud)
        Benchmark.print()
    sys.stdout = old_stdout
    output_file.close()

def main(argv):
    Benchmark.Start()
    home = os.environ['HOME']
    script_output_dir = f"{home}/.cloudmesh/eigenfaces-svm/vm_script_output_multi/"
    benchmark_output_dir = f"{home}/.cloudmesh/eigenfaces-svm/benchmark_output_multi/"

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
        num_trials = 1
        vms = []
        print(f"Running {num_trials} trials for each cloud in {clouds}")
        for cloud in clouds:
            Shell.run(f"cms set cloud={cloud}")
            for i in range(num_trials):
                vm_name = f"{cloud}-{i}"
                print(f"Creating and running test on VM {vm_name}")
                start = default_timer()
                result = Shell.run(f"{home}/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/eigenfaces-svm-full-multi-script {vm_name} > {script_output_dir}{cloud}-{i}")
                end = default_timer()
                print(f"Script on {vm_name} finished in {end - start} seconds")
                runtimes_dic[cloud].append(end-start)
                ip = Shell.run(f'cms vm ssh {vm_name} --command="which" |  grep -E -o -m 1 "([0-9]{{1,3}}[\.]){{3}}[0-9]{{1,3}}"').split()[0]
                vms.append((ip, cloud, i))
            runtimes = np.asarray(runtimes_dic[cloud])
            print (f"\n{cloud} script run time mean: {runtimes.mean()}")
            print(f"{cloud} script run time min: {runtimes.min()}")
            print(f"{cloud} script run time max: {runtimes.max()}")
            print(f"{cloud} script run time std: {runtimes.std()}\n")

        #Run tests
        with Pool(3) as p:
            p.map(test_ai_workflow, vms)

        #Delete VMs
        for cloud in clouds:
            Shell.run(f"cms set cloud={cloud}")
            for i in range(num_trials):
                Shell.run(f'cms vm terminate {cloud}-{i}')

    # Scarpe benchmark output from script outputs
    print(f'Scraping benchmarks from script output at {script_output_dir}')
    script_outputs = os.listdir(script_output_dir)
    for file in script_outputs:
        with open(f"{script_output_dir}{file}", 'r') as f:
            b = open(f"{benchmark_output_dir}{file}-benchmark", "w")
            b.write("csv,timer,status,time,sum,start,tag,uname.node,user,uname.system,platform.version\n")
            found_benchmark = False
            for line in f.readlines():
                if line.startswith("# csv,benchmark-eigenfaces-multi-cloud/test"):  # some shells return csv info twice once as error "info" and normal output
                    found_benchmark = True
                    b.write(line[2:])  # keep csv,...
            b.close()
            if not found_benchmark:
                print(f"Error on script {script_output_dir}{file}")
                if os.path.exists(f"{benchmark_output_dir}{file}-benchmark"):
                    os.remove(f"{benchmark_output_dir}{file}-benchmark")

    # Read benchmark output and compute statistics
    print(f'Reading benchmarks from benchmark output at {benchmark_output_dir}')
    columns = ["csv", "timer", "status", "time", "sum", "start", "tag", "uname.node", "user", "uname.system",
               "platform.version, cloud"]
    benchmark_df = pd.DataFrame(columns=columns)
    benchmark_outputs = os.listdir(benchmark_output_dir)
    for file in benchmark_outputs:
        cloud = file.split("-")[0]
        df = pd.read_csv(f"{benchmark_output_dir}{file}")
        df['cloud'] = cloud
        if cloud == 'aws':
            df.loc[df['uname.node'].str.startswith("ip"), ["uname.node"]] = 'aws' + "-" + file.split("-")[1]
        benchmark_df = pd.concat([benchmark_df, df])

    benchmark_df['test_type'] = 'local'
    benchmark_df.loc[benchmark_df['uname.node'] == gethostname(), ['test_type']] = 'remote'

    print("Printing trial statistics:")
    result = ""
    stats_df = pd.DataFrame(columns=['test', 'type', 'cloud', 'mean', 'min', 'max', 'std'])
    for cloud in benchmark_df['cloud'].unique():
        result += f"{cloud} has {len(benchmark_df.loc[benchmark_df['cloud'] == cloud]['uname.node'].unique())} VM samples.\n"
        for timer in benchmark_df['timer'].unique():
            for test_type in benchmark_df['test_type'].unique():
                df = benchmark_df.loc[(benchmark_df['cloud'] == cloud) & (benchmark_df['timer'] == timer) & (
                        benchmark_df['test_type'] == test_type), ['time']]
                if len(df.values) > 0:
                    mean = df.values.mean()
                    min = df.values.min()
                    max = df.values.max()
                    std = df.values.std()
                    result += f"{cloud} {timer} {test_type} samples: {len(df.values)}\n"
                    result += f"{cloud} {timer} {test_type} mean: {mean}\n"
                    result += f"{cloud} {timer} {test_type} min: {min}\n"
                    result += f"{cloud} {timer} {test_type} max: {max}\n"
                    result += f"{cloud} {timer} {test_type} std: {std}\n\n"
                    to_append = [timer, test_type, cloud, mean, min, max, std]
                    stats_series = pd.Series(to_append, index=stats_df.columns)
                    stats_df = stats_df.append(stats_series, ignore_index=True)

    print(result)

    stats_df = stats_df.round(decimals=2)
    stats_df['test'] = stats_df['test'].str.replace("benchmark-eigenfaces-multi-cloud/", "")
    # print(stats_df_print.sort_values(by=['test', 'type', 'cloud']).to_markdown(index=False))
    print(stats_df.sort_values(by=['test', 'type', 'cloud']).to_latex(index=False))

    # graph 1: stacked bar graph of all tests
    download_df = stats_df.loc[(stats_df['test'] == 'test_download_data')]
    download_means = download_df["mean"]

    download_mins = download_df["min"]
    download_stds = download_df["std"]
    download_labels = download_df["cloud"]

    train_df = stats_df.loc[(stats_df['test'] == 'test_train')]
    train_means = train_df["mean"]
    train_mins = train_df["min"]
    train_stds = train_df["std"]


    upload_df = stats_df.loc[(stats_df['test'] == 'test_upload')]
    upload_means = upload_df["mean"]
    upload_mins = upload_df["min"]
    upload_stds = upload_df["std"]

    predict_df = stats_df.loc[(stats_df['test'] == 'test_predict')]
    predict_means = predict_df["mean"]
    predict_mins = predict_df["min"]
    predict_stds = predict_df["std"]

    plt.style.use('seaborn-whitegrid')
    n = 3
    ind = np.arange(n)
    width = 0.35
    p1 = plt.bar(ind, download_means, width, yerr=download_stds, color='orange', capsize=3)
    p2 = plt.bar(ind, train_means, width, bottom=download_means, yerr=train_stds, color='green', capsize=3)
    p3 = plt.bar(ind, upload_means, width, bottom=download_means.values + train_means.values, yerr=upload_stds, color='yellow', capsize=3)
    p4 = plt.bar(ind, predict_means, width, bottom=download_means.values + train_means.values + upload_means.values, yerr=predict_stds, color='blue', capsize=3, ecolor="gray")
    plt.ylabel('Time (s)')
    plt.title('AI Service Workflow Runtime')
    plt.xticks(ind, download_labels)
    plt.legend((p1[0], p2[0],p3[0],p4[0]), ('Download Data', 'Train', 'Upload', 'Predict'), bbox_to_anchor=(0, 0), loc='lower left', ncol=4, frameon=True)
    plt.savefig('ai_service_workflow_runtime.png')
    plt.savefig('ai_service_workflow_runtime.pdf')
    plt.savefig('ai_service_workflow_runtime.svg')
    plt.show()

if __name__ == "__main__":
    main(sys.argv)
    #test_ai_workflow(("35.153.193.180", "aws", 0))
