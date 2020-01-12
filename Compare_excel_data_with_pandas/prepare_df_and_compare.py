import pandas as pd


def get_df_from_excel_data(file: str, sheet_name: str, header: iter or int, index_col: iter or int)-> pd.DataFrame:
    """
    Imports all data from specified Excel sheet into dataframe
    """
    df = pd.read_excel(file, sheet_name=sheet_name, header=header, index_col=index_col)
    return df


def move_column_inplace(df: pd.DataFrame, column: str, index: int)->None:
    """
    Moves columns under specified location index
    """
    col = df.pop(column)
    df.insert(index, col.name, col)


def prepare_multi_indexes(df: pd.DataFrame, index_name: str = 'Year', index_names: iter = ('Companies', 'Year'))->None:
    """
    Creates additional index 'Year' and gives names to indexes
    """
    df.reset_index(level=1).rename({'level_1': index_name}, axis=1)
    df.index.names = index_names


def remove_and_rename_columns(df: pd.DataFrame, remove_col_ident: str, rename_col_ident: str)->None:
    """
    Removes and renames columns that ends with a certain identifier
    """
    for column in df.columns:
        if column.endswith(remove_col_ident):
            del df[column]
        if column.endswith(rename_col_ident):
            df.rename({f'{column}': f'{column.replace(rename_col_ident, "")}'}, axis=1, inplace=True)


def prepare_dataframes(file_1: str, file_2: str)->tuple:
    """
    Uploads and reshapes dataframes into the common structure for the analysis
    """

    # get averages df
    df1_avg = get_df_from_excel_data(file=file_1, sheet_name='Analysis_averages', header=[1, 2], index_col=0)
    df1_avg = df1_avg.stack(level=0)  # arrange each year on top of each other
    prepare_multi_indexes(df1_avg)  # prepare 2 indexes ('Company' and 'Year')
    move_column_inplace(df1_avg, 'Overall', 0)  # move 'Overall' column to the front

    # get count df
    df1_cnt = get_df_from_excel_data(file=file_1, sheet_name='Analysis_count', header=[1, 2], index_col=0)
    df1_cnt = df1_cnt.stack(level=0)
    prepare_multi_indexes(df1_cnt)
    print(df1_cnt)
    move_column_inplace(df1_cnt, 'Overall', 0)

    # get general averages+count df
    df2_avg_cnt = get_df_from_excel_data(file=file_2, sheet_name='Analysis', header=1, index_col=[0, 1])

    # create 2 separate df from the general one
    df2_avg = df2_avg_cnt.copy()
    remove_and_rename_columns(df2_avg, '_cnt', '_avg')
    prepare_multi_indexes(df2_avg)

    df2_cnt = df2_avg_cnt.copy()
    remove_and_rename_columns(df2_cnt, '_avg', '_cnt')
    prepare_multi_indexes(df2_cnt)
    
    return df1_avg, df1_cnt, df2_avg, df2_cnt

