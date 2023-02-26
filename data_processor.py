import pandas as pd
from datetime import datetime
import numpy as np
import os
from format_config import InputFileName, OutputFileName

def Data_Preprocessor(Fiscal_Data): 

    date_columns = Fiscal_Data.columns[Fiscal_Data.columns.str.upper().str.contains("DATE")]
    
    def date_format(df, date_columns):
        
        data = df.copy()
        
        for col in date_columns:
            
            data[col] = pd.to_datetime(data[col]).apply(lambda x : datetime.strftime(x, format = "%Y-%m-%d") if pd.notna(x) else x)
        
        return data
    
    New_Df = date_format(Fiscal_Data, date_columns)
    
    New_Df.loc[:,'SectionId'] = ((New_Df.groupby('duns_no')['duns_no'].rank(method='first')) * -1).astype(int) 
    
    return New_Df

def main(input_directory, output_directory):
    
    list_of_files = os.listdir(input_directory)
    
    for file in  list_of_files:
        
        Fiscal_Data = pd.read_csv(input_directory + file)
        
        Result = Data_Preprocessor(Fiscal_Data)
        
        Result.to_csv(output_directory + "New_" +file )

if __name__=="__main__":
    
    main(InputFileName['input_directory'], OutputFileName['output_directory'])