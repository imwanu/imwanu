import pandas as pd
file_path='C:/Users/emily/Big Data Sample.csv'
df=pd.read_csv(file_path,encoding='utf-8')
missing=df.isnull().sum().sum()
print(f"df變數中共有 {missing} 遺漏值")
age=df['年齡'].mean().round(2)
q1=df['年齡'].quantile(q=0.01)
q25=df['年齡'].quantile(q=0.25)
q75=df['年齡'].quantile(q=0.75)
q99=df['年齡'].quantile(q=0.99)
print(f"所有年齡平均:{age}")
print(f"所有人年齡1%分位點:{q1}")
print(f"所有人年齡25%分位點:{q25}")
print(f"所有人年齡75%分位點:{q75}")
print(f"所有人年齡99%分位點:{q99}")
gender=df['性別'].value_counts()
df1=df.sort_values(by='銷售金額',ascending=False).head(10)
df2 = df1.sort_values(by=['年資', '年齡'], ascending=[False, False]).head(10)
df3=df[['姓名','性別','年齡','銷售金額']]
df4=df3[df3['性別']=='男']
df5=df3[df3['性別']=='女']
df4.loc['平均']=df4.mean(axis='index')
df5.loc['平均']=df5.mean(axis='index')
age_5=df5['年齡'].mean().round(2)
sale_5=df5['銷售金額'].mean().round(2)
df5_1=df5[(df5['年齡']<age_5) & (df5['銷售金額']>sale_5) ]
df['姓氏']=df['姓名'].str[0]
firstname_counts=df['姓氏'].value_counts().head(5)
