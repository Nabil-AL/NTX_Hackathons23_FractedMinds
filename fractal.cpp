#include <vector>
#include <iostream>
#include <chrono>
#include </usr/include/lsl_cpp.h>
#include <string>
#include <time.h>
#include <thread>

/**
 * Example program that demonstrates how to resolve a specific stream on the lab
 * network and how to connect to it in order to receive data.
 */

void printChunk(const std::vector<float> &chunk, std::size_t n_channels) {
	for (std::size_t i = 0; i < chunk.size(); ++i) {
		std::cout << chunk[i] << ' ';
		if (i % n_channels == n_channels - 1) std::cout << '\n';
	}
}

void printChunk(const std::vector<std::vector<float>> &chunk) {
	for (const auto &vec : chunk) printChunk(vec, vec.size());
}

void fractole(float t3, float t4)
{
	std::cout << "t3: " << t3 << "|t4: " << t4 << std::endl;
}

int main(int argc, char *argv[]) {
	std::string field, value;
	const int max_samples = argc > 3 ? std::stoi(argv[3]) : 10;
	if (argc < 3) {
		std::cout << "This connects to a stream which has a particular value for a "
					 "given field and receives data.\nPlease enter a field name and the desired "
					 "value (e.g. \"type EEG\" (without the quotes)):"
				  << std::endl;
		std::cin >> field >> value;
	} else {
		field = argv[1];
		value = argv[2];
	}

	// resolve the stream of interet
	std::cout << "Now resolving streams..." << std::endl;
	std::vector<lsl::stream_info> results = lsl::resolve_stream(field, value);
	if (results.empty()) throw std::runtime_error("No stream found");

	std::cout << "Here is what was resolved: " << std::endl;
	std::cout << results[0].as_xml() << std::endl;

	// make an inlet to get data from it
	std::cout << "Now creating the inlet..." << std::endl;
	lsl::stream_inlet inlet(results[0]);

	// start receiving & displaying the data
	std::cout << "Now pulling samples..." << std::endl;

	std::vector<float> sample;
	std::vector<std::vector<float>> chunk_nested_vector;
	std::vector<float> time;
	float totT3 = 0;
	float totT4 = 0;
	float maxT3 = 0;
	float maxT4 = 0;
	float minT3 = 0;
	float minT4 = 0;
	int count = 0;
	auto start{std::chrono::steady_clock::now()};
	for (int i = 0; i < max_samples; ++i) {
		// pull a single sample
		inlet.pull_sample(sample);
		printChunk(sample, inlet.get_channel_count());
		const auto end{std::chrono::steady_clock::now()};
		totT3 += sample[0];
		totT4 += sample[1];
		count += 1;
		if (sample[0] > maxT3)
			maxT3 = sample[0];
		if (sample[1] > maxT4)
			maxT4 = sample[1];
		if (i == 0)
		{
			minT3 = sample[0];
			minT4 = sample[1];
		}
		if (sample[0] < minT3)
			minT3 = sample[0];
		if (sample[1] < minT4)
			minT4 = sample[1];
		{
			using namespace std::chrono_literals;
			if (end - start > 1s)
			{

				std::cout << "lol" << std::endl;
				std::cout << "totT3: " << totT3 << "|totT4: " << totT4 << "|count: " << count << std::endl;
				auto firstAverage = ((totT3 / count) - minT3) / (maxT3 - minT3) * 4 - 2;
				auto secondAverage = ((totT4 / count) - minT4) / (maxT4 - minT4) * 4 - 2;
				fractole(firstAverage, secondAverage);
				start = std::chrono::steady_clock::now();
				totT3 = 0;
				totT4 = 0;
				count = 0;
			}

		}

		// Sleep so the outlet will have time to push some samples
		std::this_thread::sleep_for(std::chrono::milliseconds(500));

		// // pull a chunk into a nested vector - easier, but slower
		// inlet.pull_chunk(chunk_nested_vector);
		// printChunk(chunk_nested_vector);

		// std::this_thread::sleep_for(std::chrono::milliseconds(500));

		// // pull a multiplexed chunk into a flat vector
		// inlet.pull_chunk_multiplexed(sample);
		// printChunk(sample, inlet.get_channel_count());
	}
	for (int i = 0 ; i < time.size() ; i++)
		std::cout << "all time = " << time[i] << std::endl;
	if (argc == 1) {
		std::cout << "Press any key to exit. " << std::endl;
		std::cin.get();
	}
	return 0;
}
