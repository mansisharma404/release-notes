import pandas as pd
import datetime

def get_datetime_string_from_date_array(date_array: list) -> datetime:
    month_string_to_number_mapping = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
    }
    return datetime.datetime(int(date_array[5]), month_string_to_number_mapping[date_array[2]], int(date_array[3]))


def convert_date_string_into_datetime(date: str) -> datetime:
    # dd-mm-yyyy
    date_arr = date.split('-')
    return datetime.datetime(int(date_arr[2]), int(date_arr[1]), int(date_arr[0]))


def get_filtered_data(dataframe, start_date: str or None, till_date: str or None, author: str or None):
    filtered_by_start_date = dataframe
    if start_date is not None:
        filtered_by_start_date = filtered_by_start_date.loc[
            filtered_by_start_date['Timestamp'] > convert_date_string_into_datetime(start_date)]
    filtered_by_end_date = filtered_by_start_date
    if till_date is not None:
        filtered_by_end_date = filtered_by_end_date.loc[
            filtered_by_end_date['Timestamp'] < convert_date_string_into_datetime(till_date)]
    filtered_by_author = filtered_by_end_date
    if author is not None:
        filtered_by_author = filtered_by_author.loc[filtered_by_author['Author'] == author]
    return filtered_by_author


def pipeline(filename: str, start_date: str or None, till_date: str or None, author: str or None):
    df = pd.read_fwf("unparsed_logs.txt", widths=None)
    data_temp = []
    data_overall = list(data_temp)
    for index, details in df.iterrows():
        clean = str(details).replace('Details    ', '')
        clean_arr = clean.split()[:-4]
        if clean_arr[0] == 'commit':
            data_temp = [clean_arr[1]]
        elif clean_arr[0] == 'Author:':
            data_temp.append(clean_arr[1])
        elif clean_arr[0] == 'Date:':
            data_temp.append(get_datetime_string_from_date_array(clean_arr))
        elif clean_arr[-1].startswith('(#'):
            data_temp.append(clean_arr[-1])
            description = ' '.join(clean_arr[:-1])
            data_temp.append(description)
            data_overall.append(data_temp)
            data_temp = data_temp[:-2]

    del data_overall[0]
    data_frame_with_raw_data = pd.DataFrame(data_overall, columns=['commit ID', 'Author', 'Timestamp', 'PR number','Feature Description'])
    data_frame_with_filtered_data = get_filtered_data(data_frame_with_raw_data, start_date, till_date, author)
    print(data_frame_with_filtered_data['Feature Description'].to_csv(filename, index=False))

pipeline('r_notes.txt', None, None, None)
