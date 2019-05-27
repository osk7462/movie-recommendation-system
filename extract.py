import re
import csv

class Tocsv:

	def __init__(self, in_filename):
		self.in_filename = in_filename
		self.line_no = int(0)
		self.is_writable = True
		self.total_ratings = int(0)
		self.out_file_name = "dataset/ratings_"
		self.out_file_name_index = int(0)

	@staticmethod
	def _process(line):
		try:
			return (line.split(":")[1].lstrip(" ").rstrip("\n"), True)
		except:
			return ("", False)
	
	@staticmethod
	def _clean(text):
		return re.sub("<.*?>", " ", text)
	
	def get_file_name(self):
		self.out_file_name_index += 1
		return self.out_file_name + str(self.out_file_name_index) + ".csv"

	def get_writer(self):
		fieldname = ['productId', 'userId', 'rating', 'timestamp', 'summary' , 'review']
		csv_file =  open(self.get_file_name(), "w", newline="")
		writer = csv.DictWriter(csv_file, fieldnames=fieldname)
		writer.writeheader()
		return writer




	def extract(self):
		with open(in_filename, "r") as file:
			while True:
				try:
					for line in file:
						if (self.total_ratings%100000) == 0:
								writer = self.get_writer()
								print("{} rating has been recorded".format(self.total_ratings))
								self.total_ratings += 1

						if line != '\n' and self.is_writable:
							if self.line_no is 0:
								product_id, self.is_writable = self._process(line) 

							elif self.line_no is 1:
								user_id, self.is_writable = self._process(line)
							
							elif self.line_no is 4:
								rating, self.is_writable = self._process(line)
					
							elif self.line_no is 5:
								timestamp, self.is_writable = self._process(line)

							elif self.line_no is 6:
								summary, self.is_writable = self._process(line)
							
							elif self.line_no is 7:
								review, self.is_writable = self._process(line)
								review = self._clean(review)
							self.line_no += 1
						
						elif self.is_writable:
							if self.line_no is 8:
								writer.writerow({'productId': product_id, 'userId': user_id, 'rating': rating, 'timestamp':timestamp, 'summary':summary,  'review': review})
							self.line_no = 0
							self.total_ratings += 1
						elif line == '\n':
								self.is_writable = True
								self.line_no = 0
						if self.total_ratings is 7900000:
							exit(0)

				except UnicodeDecodeError:
					self.is_writable = False



if __name__ == '__main__':
	in_filename = "/home/osama/Downloads/movies.txt"
	tocsv = Tocsv(in_filename)
	tocsv.extract()
