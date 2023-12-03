import time
from pylsl import StreamInlet, resolve_stream


def fractole(second_average):
	# Do something with the data
	print(second_average)
	time.sleep(1)

def main():
	# first resolve an EEG stream on the lab network
	print("looking for an EEG stream...")
	streams = resolve_stream('type', 'EEG')

	# create a new inlet to read from the stream
	inlet = StreamInlet(streams[0])
	totT4 = 0
	maxT4 = 0
	minT4 = 0
	i = 0
	count = 0
	while True:
		# get a new sample (you can also omit the timestamp part if you're not
		# interested in it)
		sample, timestamp = inlet.pull_sample()
		print(timestamp, sample)
		if i == 0:
			minT4 = sample[0]
			start = timestamp
		count += 1
		totT4 += sample[0]
		maxT4 = max(maxT4, sample[0])
		minT4 = min(minT4, sample[0])
		if timestamp - start > 1:
			print("lol")
			second_average = max(min(((totT4 / count) - minT4) / (maxT4 - minT4) * 4 - 2, 2), -2)
			# Assuming 'fractole' is a function that needs to be defined
			fractole(second_average)
			start = time.time()
			totT3 = 0
			totT4 = 0
			count = 0
			i = 0
		else :
			i += 1

if __name__ == '__main__':
	main()
