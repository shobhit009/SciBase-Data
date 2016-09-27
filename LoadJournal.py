import json
import os.path
import csv

from py2neo import Node, Relationship, Graph, authenticate

authenticate("localhost:7474", "neo4j", "scibase")
graph = Graph("http://localhost:7474/db/data")

# Change the value of directory to the path where data to be pushed is stored
path = []
directory = '/home/shobhit/scibase/Finalized_structure'
for filename in os.listdir(directory):
	if filename.endswith(".json"):
		x = os.path.join(directory, filename)
		path.append(x)
#print path
		
count = 0
for journals in path:
	
	with open(journals) as data_file:
		json1 = json.load(data_file)
		count += 1
		#print json1.items()
		print count


#with open('TAP.json') as data_file:
#	json1 = json.load(data_file)   

#for better clarity add print statement to check each key and value pair
		tx = graph.cypher.begin()
		for key,value in json1.items():
			print key
			j=tx.graph.merge_one("Journal","Acronymn",key);
		
			for key_1,value_1 in value.items():
				if key_1 == 'ISSN':	
					print value_1		
					j[key_1] = value_1
					j.push()				
				elif (key_1 == 'Volumes'):
					for key_2,value_2 in value_1.items():
						for key_3,value_3 in value_2.items():
							for key_4,value_4 in value_3.items():
								if key_4 == 'articles':
									#print value_4.items()
									for key_5,value_5 in value_4.items():						
										for key_6,value_6 in value_5.items():
											#print key_6
											if key_6 == 'title':
												var = value_6											
												ar=tx.graph.merge_one("Article","Name",var);
												tx.graph.create_unique(Relationship(ar, "PUBLISHED_IN", j))
										for key_7,value_7 in value_5.items():		
											if key_7 == 'doi':
												x = value_7
												ar['DOI'] = value_7		
												ar.push()	

											
											elif (key_7 == 'authors'):
												for ele in value_7:												
													for key_8,value_8 in ele.items():
														if key_8 == 'name':
															var1 = value_8										
															#print var1							                  
															au=tx.graph.merge_one("Author","Name",var1);
															tx.graph.create_unique(Relationship(ar, "AUTHORED_BY", au))
													for key_9,value_9 in  ele.items():
														if key_9 == 'link':	
															l = value_9													
															au['link'] = value_9
															au.push()
										for key_10,value_10 in value_5.items():

											if key_10 == 'affiliation_data':
												#print value_10
												for ele in value_10:
												#print ele
													for key_11,value_11 in ele.items():
														
														 if key_11 == 'university':
														 	if  (value_11 != 'none' or value_11 != 'null' or value_11 != ''):
															print value_11
																#inst=tx.graph.merge_one("Affiliation","Name", value_11)
																#tx.graph.create_unique(Relationship(au, "AFFILIATED_TO", inst))
													for key_12,value_12 in ele.items():
														if key_12 == 'country':
															x = value_12
															#country=graph.merge_one("Country","Name",value_12)
															#graph.create_unique(Relationship(inst, "LOCATED_IN", country))
															#graph.create_unique(Relationship(au, "PART_OF", country))
		tx.commit()


														

										
										
											
		with open('self citation list (1)_good.csv') as journal_file:
				journal_name = csv.reader(journal_file)
				for row in journal_name:
					if (key == row[1]):
							j['Name'] = row[0] 
							j['Self citation'] = row[2]
							j['Total citation'] = row[3]
							j['NLIQ'] = row[4]
							j['ICR'] = row[5]
							j['OCQ'] = row[6]
							j['SNIP'] = row[7]
							j.push()
				