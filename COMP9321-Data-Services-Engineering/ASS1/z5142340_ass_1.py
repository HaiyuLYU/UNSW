import pandas as pd
import numpy as np
def merge_csv():
    df1 = pd.read_csv('Olympics_dataset1.csv',skiprows=1)
    df1.rename(columns = {'Unnamed: 0':'Country'}, inplace = True)
    df2 = pd.read_csv('Olympics_dataset2.csv',skiprows=1)
    df2.rename(columns = {'Unnamed: 0':'Country'}, inplace = True)
    df = pd.merge(df1,df2,on = 'Country')
    return df
def question_1():
    df = merge_csv()
    return df.head(5)
def question_2():
    df = merge_csv()
    df.set_index('Country', inplace = True)
    return df.head(1)
def question_3():
    df = merge_csv()
    df.drop(['Rubish'],axis = 1)
    return df.head(5)
def question_4():
    df = merge_csv()
    df = df.dropna(how = 'any', axis = 0)
    return df.tail(10)
def question_5():
    df = merge_csv()
    df = df.dropna(how = 'any', axis = 0)
    df= df[~df['Country'].isin(['Totals'])] 
    df['Gold_x'] = df.Gold_x.str.replace(',','').astype(int)
    id = df['Gold_x'].idxmax()
    df = df.loc[[id]]
    return df
def question_6():
    df = merge_csv()
    df = df.dropna(how = 'any', axis = 0)
    df= df[~df['Country'].isin(['Totals'])]
    df['Gold_x'] = df.Gold_x.str.replace(',','').astype(int)
    df['Gold_y'] = df.Gold_y.str.replace(',','').astype(int)
    id = (df['Gold_x'] - df['Gold_y']).abs().idxmax()
    df = df.loc[[id]]
    return df
def question_7():
    df = merge_csv()
    df.rename(columns = {'Total.1':'Total_medals'}, inplace = True)
    df = df.dropna(how = 'any', axis = 0)
    df= df[~df['Country'].isin(['Totals'])]
    df['Total_medals'] = df.Total_medals.str.replace(',','').astype(int)
    df = df.sort_values(by = ['Total_medals'], ascending=False)
    df1 = df.head(1)
    df2 = df.tail(5)
    df = pd.concat([df1,df2])
    return df
def question_8():
    df = merge_csv()
    df.rename(columns = {'Total.1':'Total_medals'}, inplace = True)
    df.rename(columns = {'Total_x':'Summer'}, inplace = True)
    df.rename(columns = {'Total_y':'Winter'}, inplace = True)
    df = df.dropna(how = 'any', axis = 0)
    df= df[~df['Country'].isin(['Totals'])]
    df['Total_medals'] = df.Total_medals.str.replace(',','').astype(int)
    df['Summer'] = df.Summer.str.replace(',','').astype(int)
    df['Winter'] = df.Winter.str.replace(',','').astype(int)
    df = df.sort_values(by = ['Total_medals'], ascending=False)
    df = df.head(10)
    df.set_index('Country', inplace = True)
    df = df[['Summer','Winter']]
    ax = df.plot.barh(title = 'Models for Summer and Winter Games', stacked=True, figsize=(10,5))
def question_9():
    df = merge_csv()
    df.rename(columns = {'Gold_y':'Gold'}, inplace = True)
    df.rename(columns = {'Silver_y':'Silver'}, inplace = True)
    df.rename(columns = {'Bronze_y':'Bronze'}, inplace = True)
    countries = ['United States', 'Australia', 'Great Britain', 'Japan', 'New Zealand']
    df = df[df['Country'].str.contains('|'.join(countries))]
    df.set_index('Country', inplace = True)
    df['Gold'] = df.Gold.str.replace(',','').astype(int)
    df['Silver'] = df.Silver.str.replace(',','').astype(int)
    df['Bronze'] = df.Bronze.str.replace(',','').astype(int)
    df = df[['Gold','Silver','Bronze']]
    ax = df.plot.bar(rot=0,figsize=(15,5))
if __name__ == "__main__":
    print(question_1())
    print(question_2())
    print(question_3())
    print(question_4())
    print(question_5())
    print(question_6())
    print(question_7())
    question_8()
    question_9()
