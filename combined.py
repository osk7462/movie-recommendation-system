import csv

class Combined:

	def __init__(self, in_file_name, file_path):
		self.in_file_name = in_file_name
		self.file_path = file_path


	def create_combined_csv(self, w1, w2):
		with open("{}/{}".format(self.file_path, self.in_file_name), 'r') as csv_file:
			csv_reader = csv.reader(csv_file)
			next(csv_reader)
			field_names =  ['user', 'item', 'rating', 'timestamp']
			with open("{}/combined.csv".format(self.file_path), "w") as csv_file1:
				csv_writer = csv.DictWriter(csv_file1, fieldnames=field_names)
				csv_writer.writeheader()
				for line in csv_reader:
					combined = ((w1 * float(line[2])) + (w2 * float(line[3])))
					csv_writer.writerow({field_names[0]: line[0], field_names[1]: line[1],\
					 field_names[2]: combined, field_names[3]: line[4]})


				print("w1 = {}, and w2 = {} successfully combined.csv created.".format(w1, w2))

	def create_rating_csv(self):
		with open("{}/{}".format(self.file_path, self.in_file_name), 'r') as csv_file:
			csv_reader = csv.reader(csv_file)
			next(csv_reader)
			field_names =  ['user', 'item', 'rating', 'timestamp']
			with open("{}/rating.csv".format(self.file_path), "w") as csv_file1:
				csv_writer = csv.DictWriter(csv_file1, fieldnames=field_names)
				csv_writer.writeheader()
				for line in csv_reader:
					csv_writer.writerow({field_names[0]: line[0], field_names[1]: line[1],\
					 field_names[2]: line[2], field_names[3]: line[4]})


				print("successfully rating.csv created.")

	def create_rev_csv(self):
		with open("{}/{}".format(self.file_path, self.in_file_name), 'r') as csv_file:
			csv_reader = csv.reader(csv_file)
			next(csv_reader)
			field_names =  ['user', 'item', 'rating', 'timestamp']
			with open("{}/rev.csv".format(self.file_path), "w") as csv_file1:
				csv_writer = csv.DictWriter(csv_file1, fieldnames=field_names)
				csv_writer.writeheader()
				for line in csv_reader:
					csv_writer.writerow({field_names[0]: line[0], field_names[1]: line[1],\
					 field_names[2]: line[3], field_names[3]: line[4]})


				print("successfully rev.csv created.")

if __name__ == '__main__':
	in_file_name = 'rev_to_rating.csv'
	file_path = 'user/dataset_to_train_and_test'
	# taking weight w1=0.6 for actual rating, w2=0.4 for analyzed rating
	w1 = 0.6
	w2 = 0.4
	combined = Combined(in_file_name, file_path)
	combined.create_combined_csv(w1, w2)
	combined.create_rating_csv()
	combined.create_rev_csv()


