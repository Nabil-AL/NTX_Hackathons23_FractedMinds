import csv

with open('07-signal_d.csv', 'r') as csv_file:
	reader = csv.reader(csv_file, delimiter=';')
	data_list = list(reader)

	cols = dict()
	cols['Time (s)'] = -1
	cols['T3'] = -1
	cols['T4'] = -1

	for i, col in enumerate(data_list[0]):
		if col in cols.keys():
			cols[col] = i

	step = 5
	next_stop = step
	resT3 = []
	resT4 = []
	count = 0
	t3 = 0
	t4 = 0
	maxT3 = 0
	maxT4 = 0
	minT3 = 0
	minT4 = 0
	for index, row in enumerate(data_list[1:]):
		time = float(row[cols['Time (s)']])
		t3 += float(row[cols['T3']])
		t4 += float(row[cols['T4']])
		count += 1
		if float(row[cols['T3']]) > maxT3:
			maxT3 = float(row[cols['T3']])
		if float(row[cols['T4']]) > maxT4:
			maxT4 = float(row[cols['T4']])
		if index == 0:
			minT3 = float(row[cols['T3']])
			minT4 = float(row[cols['T4']])
		if float(row[cols['T3']]) < minT3:
			minT3 = float(row[cols['T3']])
		if float(row[cols['T4']]) < minT4:
			minT4 = float(row[cols['T4']])
		if time >= next_stop :
			resT3.append(((t3 / count) -minT3 ) / (maxT3 - minT3) * 4 - 2)
			resT4.append(((t4 / count) -minT4 ) / (maxT4 - minT4) * 4 - 2)
			t3 = 0
			t4 = 0
			count = 0
			next_stop += step

	for i in range(len(resT3)):
		print("moyen t3", resT3[i], "moyenne t4", resT4[i])
