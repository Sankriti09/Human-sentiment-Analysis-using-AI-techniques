import pandas as pd
df_reader = pd.read_json("Clothing_Shoes_and_Jewelry.json", lines = True, chunksize = 1000000)
counter = 1

for chunk in df_reader:
    new_df = pd.DataFrame(chunk[['overall','reviewText','summary']])
    new_df1 = new_df[new_df['overall']==5].sample(4000)
    new_df2 = new_df[new_df['overall']==4].sample(4000)
    new_df3 = new_df[new_df['overall']==3].sample(8000)
    new_df4 = new_df[new_df['overall']==2].sample(4000)
    new_df5 = new_df[new_df['overall']==1].sample(4000)
    
    new_df6 = pd.concat([new_df1,new_df2,new_df3,new_df4,new_df5], axis = 0, ignore_index = True)
    
    new_df6.to_csv(str(counter)+".csv", index = False)
    
    counter = counter+1
    
from glob import glob
filenames = glob("*.csv")
dataframe = [pd.read_csv(f) for f in filenames]
frame = pd.concat(dataframe, axis = 0, ignore_index = True)

frame.to_csv("Balanced_reviews.csv", index = False)