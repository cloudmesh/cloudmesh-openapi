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

    benchmark_df['test_type'] = 'local'
    benchmark_df.loc[benchmark_df['uname.node'] == gethostname(),['test_type']] = 'remote'

    print("Printing trial statistics:")
    result = ""
    stats_df = pd.DataFrame(columns=['test', 'type', 'cloud', 'mean', 'min', 'max', 'std'])
    for cloud in benchmark_df['cloud'].unique():
        result += f"{cloud} has {len(benchmark_df.loc[benchmark_df['cloud']==cloud]['uname.node'].unique())-1} VM samples.\n"
        for timer in benchmark_df['timer'].unique():
            for test_type in benchmark_df['test_type'].unique():
                df = benchmark_df.loc[(benchmark_df['cloud'] == cloud) & (benchmark_df['timer'] == timer) & (benchmark_df['test_type'] == test_type), ['time']]
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
    stats_df['test'] = stats_df['test'].str.replace("test_030_generator_eigenfaces_svm/test_", "")
    #print(stats_df_print.sort_values(by=['test', 'type', 'cloud']).to_markdown(index=False))
    print(stats_df.sort_values(by=['test', 'type', 'cloud']).to_latex(index=False))
    #pi_series = pd.Series(["test_download_data", "local", "pi", 135.5, 135.5, 135.5, 0.0], index=stats_df.columns)
    #stats_df = stats_df.append(pi_series, ignore_index=True)
    #pi_series = pd.Series(["test_scikitlearn_train", "local", "pi", 232.0, 232.0, 232.0, 0.0], index=stats_df.columns)
    #stats_df = stats_df.append(pi_series, ignore_index=True)
    #pi_series = pd.Series(["test_train", "local", "pi", 231.0, 231.0, 231.0, 0.0], index=stats_df.columns)
    #stats_df = stats_df.append(pi_series, ignore_index=True)
    #pi_series = pd.Series(["test_upload", "local", "pi", 0.05, 0.05, 0.05, 0.0], index=stats_df.columns)
    #stats_df = stats_df.append(pi_series, ignore_index=True)
    #pi_series = pd.Series(["test_predict", "local", "pi", 0.4, 0.4, 0.4, 0.0], index=stats_df.columns)
    #stats_df = stats_df.append(pi_series, ignore_index=True)

    sorter = ['aws', 'azure', 'google', 'mac book', 'docker', 'pi 4', 'pi 3b+']
    stats_df.cloud = stats_df.cloud.astype("category")
    stats_df.cloud.cat.set_categories(sorter, inplace=True)
    stats_df = stats_df.sort_values(["cloud"])

    if "pi 3b+" in stats_df['cloud'].unique():
        cost_df = stats_df[['test', 'type', 'cloud', 'mean']]
        #cost_df['cost/s'] = 0
        #cost_df['cost'] = 0
        cost_df.loc[cost_df['cloud'] == 'aws',['cost/s']] = 0.1 / 60.0 / 60.0
        cost_df.loc[cost_df['cloud'] == 'azure', ['cost/s']] = 0.096 / 60.0 / 60.0
        cost_df.loc[cost_df['cloud'] == 'google', ['cost/s']] = 0.0949995 / 60.0 / 60.0
        cost_df.loc[cost_df['cloud'] == 'pi 3b+', ['cost/s']] = 0.006546804/ 60.0 / 60.0
        cost_df.loc[cost_df['cloud'] == 'pi 4', ['cost/s']] = 0.013324201 / 60.0 / 60.0
        cost_df['cost'] = cost_df['mean'].values * cost_df['cost/s'].values

        for test in cost_df['test'].unique():
            for type in cost_df['type'].unique():
                if type == 'remote':
                    continue
                sub_df = cost_df.loc[(cost_df['test'] == test) & (cost_df['type'] == type)]
                pi_cost = sub_df.loc[cost_df['cloud'] == 'pi 3b+', 'cost'].values
                pi_mean = sub_df.loc[cost_df['cloud'] == 'pi 3b+', 'mean'].values
                cost_inc = (sub_df['cost'].values - pi_cost) / pi_cost * 100
                mean_dec = (sub_df['mean'].values * -1 + pi_mean) / pi_mean * 100
                cost_df.loc[(cost_df['test'] == test) & (cost_df['type'] == type), ["% runtime decrease"]] = mean_dec
                cost_df.loc[(cost_df['test'] == test) & (cost_df['type'] == type), ["% cost increase"]] = cost_inc

        cost_df["% cost increase"] = cost_df["% cost increase"].round(2)
        cost_df["% runtime decrease"] = cost_df["% runtime decrease"].round(2)
        cost_df = cost_df.drop(columns='cost/s')
        #pd.set_option('display.float_format', '{:.2E}'.format)
        print(cost_df.sort_values(by=['test', 'type', 'cloud']).to_latex(index=False, formatters={'cost':'{:,.2e}'.format}))

    suffix = ""
    if "pi 3b+" in stats_df['cloud'].unique():
        suffix = "_pi"

    # graph 1: download_data_local
    download_df = stats_df.loc[(stats_df['test'] == 'download_data')]
    download_means = download_df["mean"]
    download_mins = download_df["min"]
    download_stds = download_df["std"]
    download_labels = download_df["cloud"]

    #plt.style.use('ggplot')
    plt.style.use('seaborn-whitegrid')
    x = download_labels
    x_pos = [i for i, _ in enumerate(x)]
    #plt.bar(x_pos, download_means, yerr=download_stds,capsize=3, color=["green",'orange','blue', 'red'])
    plt.bar(x_pos, download_means, yerr=download_stds, capsize=3)
    plt.xlabel("Cloud")
    plt.ylabel("Seconds")
    plt.title("Time to Download and Extract Data")
    plt.xticks(x_pos, x)
    plt.savefig(f'sample_graph_1{suffix}.png')
    plt.savefig(f'sample_graph_1{suffix}.pdf')
    plt.savefig(f'sample_graph_1{suffix}.svg')
    plt.show()


    # graph 2: scikitlearn_train vs opeanpi_scikitlearn_train
    openapi_df = stats_df.loc[(stats_df['test'] == 'train')]
    openapi_means = openapi_df['mean']
    openapi_mins = openapi_df['min']
    openapi_stds = openapi_df['std']
    openapi_labels = openapi_df['cloud']

    scikitlearn_df = stats_df.loc[(stats_df['test'] == 'scikitlearn_train')]
    scikit_means = scikitlearn_df['mean']
    scikit_mins = scikitlearn_df['min']
    scikit_stds = scikitlearn_df['std']
    scikit_labels = scikitlearn_df['cloud']


    x = openapi_labels
    ind = np.arange(len(openapi_labels))
    width = 0.35
    #openapi_handles = plt.bar(ind, openapi_means, width, yerr=openapi_stds, capsize=3, color=["green", 'orange', 'blue', 'red'])
    #scikit_handles = plt.bar(ind + width, scikit_means, width, yerr=scikit_stds, capsize=3, color=["springgreen", 'bisque', 'skyblue', 'lightcoral'])
    openapi_handles = plt.bar(ind, openapi_means, width, yerr=openapi_stds, capsize=3)
    scikit_handles = plt.bar(ind + width, scikit_means, width, yerr=scikit_stds, capsize=3)
    plt.xlabel("Cloud")
    plt.ylabel("Seconds")
    plt.title("Model Training Time")
    plt.xticks(ind + width / 2, scikit_labels)
    #plt.legend([tuple(openapi_handles), tuple(scikit_handles)], ['OpenAPI service', 'Scikit-learn example'], numpoints=1,
    #           handler_map={tuple: HandlerTuple(ndivide=None)},frameon=True)
    plt.legend(['train', 'scikitlearn train'], frameon=True)
    plt.savefig(f'sample_graph_2{suffix}.png')
    plt.savefig(f'sample_graph_2{suffix}.pdf')
    plt.savefig(f'sample_graph_2{suffix}.svg')
    plt.show()


    # graph 3: upload_local vs upload_remote
    local_df = stats_df.loc[
        (stats_df['test'] == 'upload') & (stats_df['type'] == 'local')]
    local_means = local_df['mean']
    local_mins = local_df['min']
    local_stds = local_df['std']
    local_labels = local_df['cloud']

    remote_df = stats_df.loc[
        (stats_df['test'] == 'upload') & (stats_df['type'] == 'remote')]
    remote_means = remote_df['mean']
    remote_mins = remote_df['min']
    remote_stds = remote_df['std']
    remote_labels = remote_df['cloud']

    x = local_labels
    ind = np.arange(len(local_labels))
    width = 0.35
    #local_handels = plt.bar(ind, local_means, width, yerr=local_stds, capsize=3, color=["green", 'orange', 'blue', 'red'])
    local_handels = plt.bar(ind, local_means, width, yerr=local_stds, capsize=3)
    ind = np.arange(len(remote_labels))
    #remote_handles = plt.bar(ind + width, remote_means, width, yerr=remote_stds,capsize=3,
    #        color=["springgreen", 'bisque', 'skyblue'])
    remote_handles = plt.bar(ind + width, remote_means, width, yerr=remote_stds, capsize=3)
    ind = np.arange(len(local_labels))
    plt.xlabel("Cloud")
    plt.ylabel("Seconds")
    plt.title("Upload Function Runtime")
    plt.xticks(ind + width / 2, local_labels)
    #plt.legend([tuple(local_handels), tuple(remote_handles)], ['OpenAPI server', 'Remote client'], numpoints=1,
    #           handler_map={tuple: HandlerTuple(ndivide=None)}, frameon=True)
    plt.legend(['local', 'remote'], frameon=True)
    plt.savefig(f'sample_graph_3{suffix}.png')
    plt.savefig(f'sample_graph_3{suffix}.pdf')
    plt.savefig(f'sample_graph_3{suffix}.svg')
    plt.show()

    # graph 4  predict_local vs predict_remote
    local_df = stats_df.loc[
        (stats_df['test'] == 'predict') & (stats_df['type'] == 'local')]
    local_means = local_df['mean']
    local_mins = local_df['min']
    local_stds = local_df['std']
    local_labels = local_df['cloud']

    remote_df = stats_df.loc[
        (stats_df['test'] == 'predict') & (stats_df['type'] == 'remote')]
    remote_means = remote_df['mean']
    remote_mins = remote_df['min']
    remote_stds = remote_df['std']
    remote_labels = remote_df['cloud']

    x = local_labels
    ind = np.arange(len(local_labels))
    width = 0.35
    #local_handels = plt.bar(ind, local_means, width, yerr=local_stds, capsize=3, color=["green", 'orange', 'blue', 'red'])
    local_handels = plt.bar(ind, local_means, width, yerr=local_stds, capsize=3)
    ind = np.arange(len(remote_labels))
    #remote_handles = plt.bar(ind + width, remote_means, width, yerr=remote_stds, capsize=3,
    #        color=["springgreen", 'bisque', 'skyblue'])
    remote_handles = plt.bar(ind + width, remote_means, width, yerr=remote_stds, capsize=3)
    ind = np.arange(len(local_labels))
    plt.xlabel("Cloud")
    plt.ylabel("Seconds")
    plt.title("Predict Function Runtime")
    plt.xticks(ind + width / 2, local_labels)
    #plt.legend([tuple(local_handels), tuple(remote_handles)], ['OpenAPI server', 'Remote client'], numpoints=1,
    #           handler_map={tuple: HandlerTuple(ndivide=None)}, frameon=True)
    plt.legend(['local', 'remote'],frameon=True)
    plt.savefig(f'sample_graph_4{suffix}.png')
    plt.savefig(f'sample_graph_4{suffix}.pdf')
    plt.savefig(f'sample_graph_4{suffix}.svg')
    plt.show()


    Benchmark.Stop()
    Benchmark.print()
    return

if __name__ == "__main__":
    main(sys.argv)
