import pandas as pd


def relocate_column_inplace(df: pd.DataFrame, column: str, index: int)->None:
    """
    Relocates columns under specified index
    """
    col = df.pop(column)
    df.insert(index, col.name, col)


def remove_and_rename_columns(df: pd.DataFrame, remove_col_ident: str, rename_col_ident: str)->None:
    """
    Removes and renames columns that ends with a certain identifier
    """
    for column in df.columns:
        if column.endswith(remove_col_ident):
            del df[column]
        if column.endswith(rename_col_ident):
            df.rename({f'{column}': f'{column.replace(rename_col_ident, "")}'}, axis=1, inplace=True)


def prepare_dataframes(file_1: str, file_2: str,
                       avg_sheet_name: str, cnt_sheet_name: str, general_sheet_name: str,
                       index_names: iter, overall_col_name: str,
                       averages_suffix: str, count_suffix: str)->tuple:
    """
    Uploads and reshapes dataframes into the common structure for the analysis.
    Works only for dataframes with specific structure like so:

    >> df1:
            2019                  2018
            overall metric... overall metric ...
    name1   10     10          7        7
    name2   2.5    2.5         7.25     7.25

    >> df2:
           year     metric_avg metric_cnt ...
    name1  2019     12.5        10
    name2  2019     3           15

    >> result structure:
           year     metric metric ...
    name1  2019     12.5   7
    name2  2019     3      7.25

    """

    # get averages df
    df1_avg = pd.read_excel(io=file_1, sheet_name=avg_sheet_name, header=[1, 2], index_col=0)
    df1_avg = df1_avg.stack(level=0)  # arrange each year on top of each other
    df1_avg.index.names = index_names  # adding names to indexes
    relocate_column_inplace(df1_avg, overall_col_name, 0)  # move overall column to the front

    # get count df
    df1_cnt = pd.read_excel(io=file_1, sheet_name=cnt_sheet_name, header=[1, 2], index_col=0)
    df1_cnt = df1_cnt.stack(level=0)
    df1_cnt.index.names = index_names
    relocate_column_inplace(df1_cnt, overall_col_name, 0)

    # get general averages+count df
    df2_avg_cnt = pd.read_excel(io=file_2, sheet_name=general_sheet_name, header=1, index_col=[0, 1])

    # create 2 separate df from the general one
    df2_avg = df2_avg_cnt.copy(deep=True)
    remove_and_rename_columns(df2_avg, count_suffix, averages_suffix)
    df2_avg.index.names = index_names

    df2_cnt = df2_avg_cnt.copy(deep=True)
    remove_and_rename_columns(df2_cnt, averages_suffix, count_suffix)
    df2_cnt.index.names = index_names
    
    return df1_avg, df1_cnt, df2_avg, df2_cnt

