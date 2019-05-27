import csv
from pycorenlp import StanfordCoreNLP

class Torating:

	def __init__(self, in_file_name, out_file_name):
		self.in_file_name = in_file_name
		self.out_file_name = out_file_name
		self.nlp = StanfordCoreNLP('http://localhost:9000')

	def rev_to_rating(self):
		with open(self.out_file_name, "a") as csv_file0:
			field_names = ['movie_id', 'user_id', 'actual_rating', 'review_rating']
			csv_writer = csv.DictWriter(csv_file0, fieldnames=field_names)
			# csv_writer.writeheader()
			with open(self.in_file_name, "r") as csv_file:
				csv_reader = csv.reader(csv_file)
				next(csv_reader)
				row = int(0)
				for line in csv_reader:
					vpos = int(0)
					vneg = int(0)
					sentValue = int(0)
					text = str(line[4]) + ". " + str(line[5])
					resul = self.nlp.annotate(text, properties={
						'annotators': 'sentiment',
						'outputFormat': 'json',
						'timeout': '500000'
						})

					for s in resul["sentences"]:
						if s["sentiment"] == 'Verypositive':
							vpos += 1
						if s["sentiment"] == "Verynegative":
							vneg += 1
						sentValue += int(s["sentimentValue"]) + 1
						if s["index"] == 0:
							s["index"] = 1
					rev_rating = ((sentValue / s["index"]) + (0.5 * vpos) - (0.5 * vneg))
					if rev_rating > 5:
						rev_rating = 5
					csv_writer.writerow({'movie_id': line[0], 'user_id': line[1], 'actual_rating': line[2], 'review_rating': rev_rating})
					print("{} reviews has been converted to ratings".format(row))
				row += 1

	def rev_to_rat_with_timestamp(self):
		csv_file_rating = open(self.in_file_name, 'r')
		csv_rating_reader = csv.reader(csv_file_rating)
		next(csv_rating_reader)
		field_names = ['user', 'item', 'actual_rating','review_rating', 'timestamp']
		with open('user/dataset_to_train_and_test/rev_to_rating.csv', 'w') as csv_write_file:
			csv_writer = csv.DictWriter(csv_write_file, fieldnames=field_names)
			csv_writer.writeheader()
			with open(self.out_file_name, 'r') as csv_rev_to_rat:
				csv_rev_to_rat = csv.reader(csv_rev_to_rat)
				next(csv_rev_to_rat)
				for line in csv_rev_to_rat:
					csv_writer.writerow({'user': line[1], 'item': line[0], 'actual_rating':line[2], 'review_rating': line[3], 'timestamp': next(csv_rating_reader)[3]})

		print("successfully created user/dataset_to_train_and_test/rev_to_rating.csv")
		csv_file_rating.clos()


if __name__ == '__main__':
	in_file = "user/rating.csv"
	out_file = "user/rev_to_rating.csv"
	torating = Torating(in_file, out_file)
	# torating.rev_to_rating()
	torating.rev_to_rat_with_timestamp()