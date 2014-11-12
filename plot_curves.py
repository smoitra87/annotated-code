import numpy as np
from matplotlib import pyplot as plt



if __name__ == '__main__':
	from argparse import ArgumentParser
	parser = ArgumentParser(description="Plots results from exps")
	parser.add_argument("--result_files", nargs="+", type=str)
	parser.add_argument("--descriptions", nargs="+", type=str)
	parser.add_argument("--title", type=str)
	parser.add_argument("--outf", type=str)
	args = parser.parse_args()
	assert len(args.result_files) == len(args.descriptions)

	fig, ax = plt.subplots(figsize=(12,12))
	for f, description in zip(args.result_files,args.descriptions):
		with open(f) as fin:
			epochs, train_err, valid_err = zip(*[map(float,l.strip().split()) for l in fin])
			ax.plot(epochs, train_err, label=description+"|"+"TrainErr")
			ax.plot(epochs, valid_err, '--', label=description+"|"+"ValidErr")

	ax.set_ylabel("Error")
	ax.set_xlabel("Epochs")
	ax.set_title(args.title)
	ax.grid()
	ax.legend()
	plt.savefig(args.outf)
	plt.close()


