import argparse
import matplotlib.pyplot as plt
from env import Env
import signal


def run(size, threshold):
    throughput_data_x = throughput_data_y = []

    return throughput_data_x, throughput_data_y


def plot_graph_pdf(x, y, yerror):
#     print("Generating Graph...")
    plt.figure()
    # print(x, y, yerror)
    plt.errorbar(x, y, xerr=0, yerr=yerror, ecolor='red', fmt=':', capsize=8)
    # plt.title("Throughput of a Paxos")
    plt.xlabel('Number of replicas')
    plt.ylabel('Accepted proposals per second')
    plt.savefig("output.pdf")
    return


def getExecutionMetrics(e, clusterSize, requests):
    e.setReplicaCount(clusterSize)
    e.setRequestCount(requests)
    e.run()
    # print(e.get_execution_time())
    t = e.get_execution_time()
    output_count = e.get_successful_events()
    # print(t, output_count)
    # e._graceexit(0)
    _throughput, _stddev = e.get_throughput()
    signal.signal(signal.SIGINT, e.terminate_handler)
    signal.signal(signal.SIGTERM, e.terminate_handler)

    return _throughput, _stddev


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'integers', metavar='int', type=int, choices=range(10),
    #      nargs='+', help='an integer in the range 0..9')
    parser.add_argument(
        '--size', metavar='int', type=int, default=2,
        help='number of cluster in Paxos, default 2')
    parser.add_argument(
        '--threshold', metavar='int', type=int, default=2,
        help='upper threshold of concurrent clients, default 2')
# Initialized arguments
    args = vars(parser.parse_args())
    # print(args)
    no_of_cluster = args.get('size')
    threshold_request = args.get('threshold')

    plotdata_x = []
    plotdata_y = []
    yerror = []

    y = []
    for i in range(2,no_of_cluster+1,1):
        # print(i)
        plotdata_x.append(i)
        e = Env()
        y.append(getExecutionMetrics(e, i,threshold_request))

        # print("From loop ", a, b)
        # e._graceexit(0)
    # print(plotdata_x)
    # print(getExecutionMetrics(no_of_cluster, threshold_request))
    for a,b in y:
        # print(a,b)
        plotdata_y.append(a)
        yerror.append(b)
    # print(y)
    # Launch Paxos cluster
    # plotdata_x, plotdata_y = run(no_of_cluster, threshold_request)
    # print(plotdata_y)
    # print(yerror)

# Plot Graph
    plot_graph_pdf(plotdata_x, plotdata_y, yerror)
    e._graceexit(0)

# Exit

