import pandas as pd
from prepare_df_and_compare import prepare_dataframes


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

file_path_1 = "Data_Separate_Tables.xlsx"
file_path_2 = "Data_General_Table.xlsx"

df1_avg, df1_cnt, df2_avg, df2_cnt = prepare_dataframes(file_1=file_path_1,
                                                        file_2=file_path_2,
                                                        avg_sheet_name='Analysis_averages',
                                                        cnt_sheet_name='Analysis_count',
                                                        general_sheet_name='Analysis')

print(df1_avg)
print(df1_cnt)
print(df2_avg)
print(df2_cnt)
