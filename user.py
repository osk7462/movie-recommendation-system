import csv
from collections import defaultdict


class User:

	def __init__(self, out_file_name):
		self.out_file_name = out_file_name

	def read_users(self, filename, users,movies):
		with open(filename, "r") as csv_file:
			csv_reader = csv.reader(csv_file)
			self.header = next(csv_reader)
			for line in csv_reader:
				if len(users) <= 15000 and line[0] in movies.keys():
					users[line[1]].append(line)
					continue

				if line[1] in users.keys() and line[0] in movies.keys():
					users[line[1]].append(line)

	def _create_csv(self, users):
		with open(self.out_file_name, 'w', newline='') as csv_file:
			csv_writer = csv.DictWriter(csv_file, fieldnames=self.header)
			csv_writer.writeheader()
			for keys in users.keys():
				for row in users[keys]:
					csv_writer.writerow({self.header[0]:row[0], self.header[1]: row[1], self.header[2]: row[2],\
					 self.header[3]: row[3],self.header[4]: row[4], self.header[5]: row[5]})

	def get_movies(self, filename, movies):
		with open(filename, "r") as csv_file:
			csv_reader = csv.reader(csv_file)
			next(csv_reader)
			for line in csv_reader:
				movies[line[0]] = None
				if len(movies.keys()) > 12000:
					break
				
	

if __name__ == '__main__':
	out_file_name = "user/rating.csv"
	users = defaultdict(list)
	movies = defaultdict(list)
	user = User(out_file_name)
	for i in range(35):
		in_file_name = "dataset/ratings_" + str(i+1) + '.csv'
		user.get_movies(in_file_name, movies)
		print("{} files has been read".format(i+1))
	for i in range(35):
		in_file_name = "dataset/ratings_" + str(i+1) + '.csv'
		user.read_users(in_file_name, users, movies)
		print("{} files has been read".format(i+1))
	user._create_csv(users)



