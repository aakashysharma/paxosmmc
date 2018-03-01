import argparse
import matplotlib.pyplot as plt


def run(size, threshold):
    throughput_data_x = throughput_data_y = []

    return throughput_data_x, throughput_data_y


def plot_graph_pdf(x, y):
    plt.figure()
    plt.errorbar(x, y, xerr=0.2, yerr=0.4)
    plt.title("Throughput of a Paxos")
    plt.xlabel('Number of clusters')
    plt.ylabel('Throughput')
    plt.savefig("output.pdf")
    return







if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'integers', metavar='int', type=int, choices=range(10),
    #      nargs='+', help='an integer in the range 0..9')
    parser.add_argument(
        '--size', metavar='int', type=int, default=3,
        help='number of cluster in Paxos, default 3')
    parser.add_argument(
        '--threshold', metavar='int', type=int, default=2,
        help='upper threshold of concurrent clients, default 2')
# Initialized arguments
    args = vars(parser.parse_args())
    # print(args)
    no_of_cluster = args.get('size')
    threshold_request = args.get('threshold')

# Launch Paxos cluster
    plotdata_x, plotdata_y = run(no_of_cluster, threshold_request)

# Plot Graph
    plot_graph_pdf(plotdata_x,plotdata_y)

# Exit

