import numpy as np

#
# Constants
#

AA_CODES = 'A,R,N,D,C,Q,E,G,H,I,L,K,M,F,P,S,T,W,Y,V'.split(',')
aadict = dict([(aa, i) for i, aa in enumerate(AA_CODES)])
datadir = "data"
PLOTTING = True

#
# Helper Functions
#


def write_matrix_act(mat, fname):
    """ Given a numpy ndarray write a """
    mat.dtype = 'int'
    with open(fname, 'w') as fout:
        for row in mat:
            print >> fout, "".join(map(str, row))


def write_fasta_matrix(mat, fname):
    """
    Given a datamatrix file writes a fasta file
    """
    with open(fname, 'w') as fout:
        assert len(mat.shape) == 2
        for seqid, seq in enumerate(mat):
            print >> fout, ">seq"+str(seqid+1)
            print >> fout, "".join([num_to_aacode(numcode) for numcode in seq])


def convert_mat_from_msa(msaf):
    """ Convert a MSA file into numeric format used by DRBM"""

    mat = []
    with open(msaf) as fin:
        mat.append([map(aacode_to_num, line.strip()) for line in fin])
    return np.asarray(mat, dtype="int").squeeze()


def convert_mat_from_sample(msaf):
    """ Convert a MSA file into numeric format used by DRBM"""

    mat = []
    with open(msaf) as fin:
        for line in fin:
            mat.append(map(int, line.strip()))
    return np.asarray(mat, dtype="int").squeeze()


def num_to_chr(num):
    # cast num
    num = int(num)
    assert isinstance(num, int)
    return chr(97+num)


def num_to_aacode(num):
    global AA_CODES
    return AA_CODES[num]


def aacode_to_num(num):
    return aadict[num]

"""
Demo of a function to create Hinton diagrams.

Hinton diagrams are useful for visualizing the values of a 2D array (e.g.
a weight matrix): Positive and negative values are represented by white and
black squares, respectively, and the size of each square represents the
magnitude of each value.

Initial idea from David Warde-Farley on the SciPy Cookbook
"""
if PLOTTING == True:

    import numpy as np
    import matplotlib.pyplot as plt

    def hinton(matrix, max_weight=None, ax=None, fname=None, title=None):
        """Draw Hinton diagram for visualizing a weight matrix."""
        ax = ax if ax is not None else plt.gca()

        if title is not None:
            ax.title(title)
        else:
            plt.title("Hinton Weight plot")

        plt.xlabel("Hidden Unit")
        plt.ylabel("Visible Unit")

        if not max_weight:
            max_weight = 2**np.ceil(np.log(np.abs(matrix).max())/np.log(2))

        ax.patch.set_facecolor('gray')
        ax.set_aspect('equal', 'box')
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())

        for (x, y), w in np.ndenumerate(matrix):
            color = 'white' if w > 0 else 'black'
            size = np.sqrt(np.abs(w))
            rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                                 facecolor=color, edgecolor=color)
            ax.add_patch(rect)

        ax.autoscale_view()
        ax.invert_yaxis()

        if fname is not None:
            plt.savefig(fname)

    def grayscale_prob(matrix, fname=None, title="None"):
        """
        Plot a 2D plot of a matrix
        """
        assert len(matrix.shape) == 2
        fig, ax = plt.subplots()

        ax.imshow(matrix, cmap=plt.cm.gray, interpolation='nearest')
        ax.set_title('Probability Matrix')

        # Move left and bottom spines outward by 10 points
        ax.spines['left'].set_position(('outward', 10))
        ax.spines['bottom'].set_position(('outward', 10))
        # Hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')

        if fname is not None:
            plt.savefig(fname)

    def plot_iter_metrics(metric_best_iter, fn, metrics):

        import numpy as np
        import matplotlib.pyplot as plt

        # Example data
        x = range(0, 100, 10) + range(100, 1001, 100)
        # Create plots with pre-defined labels.
        # Alternatively, you can pass labels explicitly when calling `legend`.
        fig, ax = plt.subplots()
        for metric in metrics:
            traj = metric_best_iter[metric]
            ax.plot(np.log10(10+np.asarray(x)), traj, label=metric)

        # x1,x2,y1,y2 = plt.axis()
        # plt.axis((x1,x2,y1,y2+10))
        # y1,y2 = plt.ylim()
        # plt.ylim((050))

        plt.xlabel('Log10(Iterations)')
        plt.ylabel('Metrics')
        plt.title('Learning Progress Best Model')

        # Now add the legend with some customizations.
        legend = ax.legend(loc='upper right', shadow=True)

        # The frame is matplotlib.patches.Rectangle instance surrounding the
        # legend.
        plt.savefig(fn)
        plt.close()


if __name__ == '__main__':
    # hinton(np.random.rand(20, 20) - 0.5)
    # grayscale_prob(np.random.uniform(size=(20, 20)))
    # plt.show()
    pass
