import json
import os.path
from pprint import pprint
from string import digits
import re, math
from collections import Counter
import operator
import matplotlib.pyplot as plt
from pylab import *

pos = arange(30)+.5
l = []
#l1 = []
count = 0
dic = {}

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])
	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	#print sum1
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	#print sum2
	denominator = math.sqrt(sum1) * math.sqrt(sum2)
	#print denominator
	 #print "denominator : " + str(denominator) + "  numerator: " + str(numerator)
	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator
	
def text_to_vector(text):
	words = WORD.findall(text)
	return Counter(words)

def freq(var):
	if not dic:
		dic[var]=1
	else:
		for key,value in dic.items():
			cosine = get_cosine(text_to_vector(key), text_to_vector(var))
			if (cosine > 0.7):
				count = dic[key]
				count+=1
				dic[key] = count
			else:
				dic[var]=1
		return dic		
		

def graph(d):

	plt.barh(pos, d.values(), align='center')
	plt.yticks(pos, (d.keys()))

	#plt.barh(range(len(d)), d.values(), align='center')
	#plt.yticks(range(len(d)), (d.keys()))

	for i,v in enumerate(d.values()):
		text(v + .2, i + .25, str(v), fontweight = 'bold', fontsize = '8')
	xlim(0, 40)

	plt.xlabel('frequency', fontsize=18)
	plt.ylabel('keywords', fontsize=18)
	plt.title('Keywords v/s frequency',fontsize =20)

	plt.show()	

def top30(x):
	sorted_dictionary = sorted(dic.items(), key=operator.itemgetter(1) , reverse=True)
	for items in sorted_dictionary[:30:]:
		l.append(items)
		new_dic= dict(l)
	return new_dic		


path = []
directory = '/home/shobhit/Query'
for filename in os.listdir(directory):
	if filename.endswith("Article 4v2.json"):
		#print filename
		x = os.path.join(directory, filename)
		path.append(x)
#print path
		
#count = 0
for journals in path:
	#print journals

	with open(journals) as data_file:
		json1 = json.load(data_file)

		for key,value in json1.items():
			#print key
			if key == "details":
				for key_1,value_1 in value.items():
					#print key_1
					if key_1 == "keywords":
						for ele in value_1:
							for key_2,value_2 in ele.items():
								if key_2 == "kwd":
									for ele in value_2:
										var = ele.lower()
										#l.append(var)
										freq(var)

			   
			elif key == "referenced_articles":
				for ele in value:
					for key,value in ele.items():
						#print key
						if key == "details":
							for key_1,value_1 in value.items():
								if key_1 == 'keywords':
									for ele in value_1:
										for key_2,value_2 in ele.items():
											if key_2 == "kwd":
												for ele in value_2:
													var = ele.lower()
													#l1.append(var1)
													freq(var)
					
graph(top30(dic))
