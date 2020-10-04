import pandas as pd
import numpy as np

today = pd.to_datetime('today').strftime('%Y-%m-%d')
company = pd.read_csv('./data/company_info_{0}.csv'.format(today))

converted = pd.DataFrame()
converted[company.columns[0]] = company[company.columns[0]]

for i in range(1,len(company.columns)):
    if i != 4:
        converted[company.columns[i]] = [j.replace(',','') for j in company[company.columns[i]]]
        converted[company.columns[i]] = [j.replace('--','') for j in converted[company.columns[i]]]
        converted[company.columns[i]] = [np.float32(j) if j != '' else np.nan for j in converted[company.columns[i]]]
    elif i == 4:
        converted[company.columns[i]] = company[company.columns[i]]

converted.to_csv('./data/company_convert_{0}.csv'.format(today), index=False)

# can change the list as needed
focus_df = converted[[
    'company_code',
    'Revenue Growth Rate (5Y)',
    'Revenue Growth Rate (3Y)',
    '10 Day Average Trading Volume',
    '3 Month Average Trading Volume',
    'Net Profit Margin (5Y)',
    'Net Profit Margin Growth Rate (5Y)']]

stats = focus_df.describe()
selected_companies = focus_df[
        (focus_df['Revenue Growth Rate (5Y)'] > stats.iloc[5,0]) & \
        (focus_df['Revenue Growth Rate (3Y)'] > stats.iloc[5,1]) & \
        (focus_df['10 Day Average Trading Volume'] >= stats.iloc[5,2]) & \
        (focus_df['3 Month Average Trading Volume'] >= stats.iloc[5,3]) & \
        (focus_df['Net Profit Margin (5Y)'] > stats.iloc[5,4]) & \
        (focus_df['Net Profit Margin Growth Rate (5Y)'] > 0)
        ].copy()

# selected_companies.describe()

selected_companies.to_csv('./data/selected_companies_{0}.csv'.format(today), index=False)
