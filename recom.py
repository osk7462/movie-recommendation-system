from surprise import SVD, SVDpp
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from combined import Combined
from surprise.model_selection import train_test_split
from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline, BaselineOnly
import heapq
from collections import defaultdict
from operator import itemgetter

class Recomm:

	def __init__(self, filePath):
		self.file_path = filePath

	def Evaluate_svd(self, file_name):
		reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
		data = Dataset.load_from_file(self.file_path+"/{}".format(file_name), reader=reader)
		trainset, testset = train_test_split(data, test_size=.25)
		
		# using svdpp algorithm.
		algo = SVDpp()
		algo.fit(trainset)
		predictionsSvdpp = algo.test(testset)
		# pred = algo.predict(uid='A141HP4LYPWMSR', iid='B003BGZ60Y')
		# print(pred)

		# using svd algorith.
		algo = SVD()
		algo.fit(trainset)
		predictions = algo.test(testset)

		return { "svd" : (accuracy.mae(predictions),  accuracy.rmse(predictions)),\
		 "SVDpp": (accuracy.mae(predictionsSvdpp),accuracy.rmse(predictionsSvdpp))}

	
	def Evaluate_baseline(self, file_name):
		reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
		data = Dataset.load_from_file(self.file_path+"/{}".format(file_name), reader=reader)
		trainset, testset = train_test_split(data, test_size=.25)
		model = BaselineOnly(bsl_options={'method': 'als',
               'n_epochs': 5,
               'reg_u': 12,
               'reg_i': 5})
		model.fit(trainset)
		predictions_Baselineonly = model.test(testset)

		model = BaselineOnly(bsl_options={'method': 'sgd',
               'learning_rate': .00005,
               })
		model.fit(trainset)
		predictions_Baselineonlysgd = model.test(testset)

		return {
				"BaselineOnly_als": (accuracy.mae(predictions_Baselineonly),  accuracy.rmse(predictions_Baselineonly)),
				"BaselineOnly_sgd": (accuracy.mae(predictions_Baselineonlysgd),  accuracy.rmse(predictions_Baselineonlysgd))
				}




	
	def Evaluate_sim(self, file_name, sim_module):
		reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
		data = Dataset.load_from_file(self.file_path+"/{}".format(file_name), reader=reader)
		trainset, testset = train_test_split(data, test_size=.25)
		sim_options = {'name': sim_module,
               'user_based': True
               }
		model = KNNBasic(sim_options=sim_options)
		model.fit(trainset)
		predictions_knnbasic = model.test(testset)

		model = KNNWithMeans(sim_options=sim_options)
		model.fit(trainset)
		predictions_knnwithmeaans = model.test(testset)

		model = KNNWithZScore(sim_options=sim_options)
		model.fit(trainset)
		predictions_KNNWithZScore = model.test(testset)

		model = KNNBaseline(sim_options=sim_options)
		model.fit(trainset)
		predictions_KNNBaseline = model.test(testset)



		return {"KNNBasic":(accuracy.mae(predictions_knnbasic),  accuracy.rmse(predictions_knnbasic)),
				"KNNBaseline": (accuracy.mae(predictions_KNNBaseline),  accuracy.rmse(predictions_KNNBaseline)),
				"KNNWithZScore":(accuracy.mae(predictions_KNNWithZScore),  accuracy.rmse(predictions_KNNWithZScore)),
				"KNNWithMeans": (accuracy.mae(predictions_KNNWithZScore),  accuracy.rmse(predictions_KNNWithZScore)),
				}



if __name__ == '__main__':
	in_file_name = 'rev_to_rating.csv'
	file_path = 'user/dataset_to_train_and_test'
	combined = Combined(in_file_name, file_path)
	recomm = Recomm('user/dataset_to_train_and_test')
	
	# for baseline 
	with open("Baseline.txt", "w") as result:
		result.write('{}On actual rating{}\n'.format("*"*67, "*"*68))
		print("on actual rating.....")
		res = recomm.Evaluate_baseline("rating.csv")
		result.write("BaselineOnly_als\nMAE:{}\tRMSE:{}\n".format(res['BaselineOnly_als'][0], res['BaselineOnly_als'][1]))
		result.write("BaselineOnly_sgd\nMAE:{}\tRMSE:{}\n".format(res['BaselineOnly_sgd'][0], res['BaselineOnly_sgd'][1]))

		print("on review rating.....")
		result.write('{}On actual rating{}\n'.format("*"*67, "*"*68))
		res = recomm.Evaluate_baseline("rev.csv")
		result.write("BaselineOnly_als\nMAE:{}\tRMSE:{}\n".format(res['BaselineOnly_als'][0], res['BaselineOnly_als'][1]))
		result.write("BaselineOnly_sgd\nMAE:{}\tRMSE:{}\n".format(res['BaselineOnly_sgd'][0], res['BaselineOnly_sgd'][1]))


		result.write('{}On combined rating{}\n'.format("*"*67, "*"*65))
		print("on combined rating .....")
		for i in range(1,10):
			w1 = i/10;
			w2 = 1-w1;
			combined.create_combined_csv(w1,w2)
			result.write("W1 = {}\tW2 = {}\n".format(w1,w2))
			res = recomm.Evaluate_baseline("combined.csv")
			result.write("BaselineOnly_als\nMAE:{}\tRMSE:{}\n".format(res['BaselineOnly_als'][0], res['BaselineOnly_als'][1]))
			result.write("BaselineOnly_sgd\nMAE:{}\tRMSE:{}\n".format(res['BaselineOnly_sgd'][0], res['BaselineOnly_sgd'][1]))

	# for svd and svdpp
	with open("svd_svdpp.txt", 'w') as result:
		result.write('{}On actual rating{}\n'.format("*"*67, "*"*68))
		print("on actual rating.....")
		res = recomm.Evaluate_svd("rating.csv")
		result.write("svd\nMAE:{}\tRMSE:{}\n".format(res['svd'][0], res['svd'][1]))
		result.write("svdPP\nMAE:{}\tRMSE:{}\n".format(res['SVDpp'][0], res['SVDpp'][1]))
		
		print("on review rating.....")
		result.write('{}On actual rating{}\n'.format("*"*67, "*"*68))
		res = recomm.Evaluate_svd("rev.csv")
		result.write("svd\nMAE:{}\tRMSE:{}\n".format(res['svd'][0], res['svd'][1]))
		result.write("svdPP\nMAE:{}\tRMSE:{}\n".format(res['SVDpp'][0], res['SVDpp'][1]))
		
		result.write('{}On combined rating{}\n'.format("*"*67, "*"*65))
		print("on combined rating .....")
		for i in range(1,10):
			w1 = i/10;
			w2 = 1-w1;
			combined.create_combined_csv(w1,w2)
			result.write("W1 = {}\tW2 = {}\n".format(w1,w2))
			res = recomm.Evaluate_svd("combined.csv")

			result.write("svd\nMAE:{}\tRMSE:{}\n".format(res['svd'][0], res['svd'][1]))
			result.write("svdPP\nMAE:{}\tRMSE:{}\n".format(res['SVDpp'][0], res['SVDpp'][1]))
			
	# for similarity modules

	for sim_module in ("cosine", "msd", "pearson"):
		with open("{}.txt".format(sim_module), 'w') as result:
			result.write('{}On actual rating{}\n'.format("*"*67, "*"*68))
			print("on actual rating.....")
			res = recomm.Evaluate_sim("rating.csv", sim_module)
			result.write("KNNBasic\nMAE:{}\tRMSE:{}\n".format(res['KNNBasic'][0], res['KNNBasic'][1]))
			result.write("KNNBaseline\nMAE:{}\tRMSE:{}\n".format(res['KNNBaseline'][0], res['KNNBaseline'][1]))
			result.write("KNNWithZScore\nMAE:{}\tRMSE:{}\n".format(res['KNNWithZScore'][0], res['KNNWithZScore'][1]))
			result.write("KNNWithMeans\nMAE:{}\tRMSE:{}\n".format(res['KNNWithMeans'][0], res['KNNWithMeans'][1]))
			
			print("on review rating.....")
			result.write('{}On actual rating{}\n'.format("*"*67, "*"*68))
			res = recomm.Evaluate_sim("rev.csv", sim_module)
			result.write("KNNBasic\nMAE:{}\tRMSE:{}\n".format(res['KNNBasic'][0], res['KNNBasic'][1]))
			result.write("KNNBaseline\nMAE:{}\tRMSE:{}\n".format(res['KNNBaseline'][0], res['KNNBaseline'][1]))
			result.write("KNNWithZScore\nMAE:{}\tRMSE:{}\n".format(res['KNNWithZScore'][0], res['KNNWithZScore'][1]))
			result.write("KNNWithMeans\nMAE:{}\tRMSE:{}\n".format(res['KNNWithMeans'][0], res['KNNWithMeans'][1]))
			

			result.write('{}On combined rating{}\n'.format("*"*67, "*"*65))
			print("on combined rating .....")
			for i in range(1,10):
				w1 = i/10;
				w2 = 1-w1;
				combined.create_combined_csv(w1,w2)
				result.write("W1 = {}\tW2 = {}\n".format(w1,w2))
				res = recomm.Evaluate_sim("combined.csv", sim_module)

				result.write("KNNBasic\nMAE:{}\tRMSE:{}\n".format(res['KNNBasic'][0], res['KNNBasic'][1]))
				result.write("KNNBaseline\nMAE:{}\tRMSE:{}\n".format(res['KNNBaseline'][0], res['KNNBaseline'][1]))
				result.write("KNNWithZScore\nMAE:{}\tRMSE:{}\n".format(res['KNNWithZScore'][0], res['KNNWithZScore'][1]))
				result.write("KNNWithMeans\nMAE:{}\tRMSE:{}\n".format(res['KNNWithMeans'][0], res['KNNWithMeans'][1]))
				