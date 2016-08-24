import json

from py2neo import Node, Relationship, Graph, authenticate

authenticate("localhost:7474", "neo4j", "scibase")
graph = Graph("http://localhost:7474/db/data")


with open('TAP.json' ) as data_file:
	json1 = json.load(data_file)

#for better clarity add print statement to check each key and value pair
	
	for key,value in json1.items():
		#print key
		j_name=graph.merge_one("Journal","Name",key);
		
		for key_1,value_1 in value.items():
			if key_1 == 'Volumes':
				for key_2,value_2 in value_1.items():
					for key_3,value_3 in value_2.items():
						for key_4,value_4 in value_3.items():
							if key_4 == 'articles':
								for key_5,value_5 in value_4.items():
									for key_6,value_6 in value_5.items():
										if key_6 == 'title':
											var = value_6
											
											ar_name=graph.merge_one("Article","Name",var);
											graph.create_unique(Relationship(ar_name, "PUBLISHED_IN", j_name))			
										
										elif (key_6 == 'authors'):
											#print value_6
											for ele in value_6:
												for key_7,value_7 in ele.items():
														if key_7 == 'name':
															var1 = value_7
															print var1

											
													
															au_name=graph.merge_one("Author","Name",var1);

															graph.create_unique(Relationship(ar_name, "AUTHORED_BY", au_name))

										
												
											
