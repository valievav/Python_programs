import pandas as pd
from prepare_df_and_compare import prepare_dataframes


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

file_path_1 = r"D:\PYTHON Practice\Testing_data_from_2_excel_files_PANDAS\Old_method.xlsx"
file_path_2 = r"D:\PYTHON Practice\Testing_data_from_2_excel_files_PANDAS\New_method.xlsx"

df1_avg, df1_cnt, df2_avg, df2_cnt = prepare_dataframes(file_path_1, file_path_2)

print(df1_avg)
print(df1_cnt)
print(df2_avg)
print(df2_cnt)
