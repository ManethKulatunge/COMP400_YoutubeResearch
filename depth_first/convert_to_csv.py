#Predict here refers to the prediction algorithm made by
#our text classification algorithm, so attach this script 
#to the bottom of our model notebook to retrieve results

import json
import csv 
from collections import defaultdict

json_data = []
for i in range(1,41):
  json_file = 'dfs_'+str(i)+'.json'
  csv_file = 'dfs_'+str(i)+'.csv'
  print(json_file)
  with open(json_file) as json_file:
      json_data = json.load(json_file)
  
      # Print the type of data variable
      print(json_data)

  header = ['dive', 'ply', 'conspiracy', 'non_conspiracy']

  conspiracy_dict = defaultdict(int)
  non_conspiracy_dict = defaultdict(int)


  for value in json_data:
    print(value)

  dive = {0:(), 1:(), 2:()}
  dive_val = 0
  for value in json_data:
      ply = 1
      for record in json_data[value]:
        if (predict(record[0]) == 'Conspiracy'):
          conspiracy_dict[ply] += 1
        else:
          non_conspiracy_dict[ply] += 1
        
        for video in record[1]:
          if (predict(video) == 'Conspiracy'):
            conspiracy_dict[ply] += 1
          else:
            non_conspiracy_dict[ply] += 1

        ply+=1
      dive[dive_val] = (conspiracy_dict, non_conspiracy_dict)
      conspiracy_dict = defaultdict(int)
      non_conspiracy_dict = defaultdict(int)
      dive_val+=1
  print(dive)

  with open(csv_file, 'w', encoding='UTF8') as f:
      writer = csv.writer(f)

      # write the header
      writer.writerow(header)
      for dive_i in range(3):
        for i in range(1,6):
          writer.writerow([dive_i, i, dive[dive_i][0][i],dive[dive_i][1][i]])