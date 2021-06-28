#%%
import pandas as pd
import sqlalchemy as sqldb
engine = sqldb.create_engine('mssql+pyodbc://LAPTOP-TTIP97EM\SQLEXPRESS/CompaniesData?driver=SQL Server?Trusted_Connection=yes')
#%%
companies_data = pd.read_excel("financial_data.xlsx")
# %%
def export_to_sql(df, tbl_name):
    """
    export_to_sql(df, name) exports a DF to an SQL DB.table, the df represents the DataFrame and Name represents the table name
    """
    df.to_sql(tbl_name, con=engine, index=False, if_exists='append')
    print(tbl_name + " exported successfully!")

#%%
financial_data = pd.DataFrame(columns=['cui', 'year', 'cifra_afaceri', 'profit_net', 'datorii', 'act_imob', 'act_circ', 'cap', 'angajati'])

#%%
for index, row in companies_data.iloc[86000:98525].iterrows():
    print(index)
    splitted_row = row[-1].split('\n')
    del(splitted_row[0])
    for data_year in splitted_row:
        the_row = []
        a = data_year.split("  ")
        for i in range(len(a)):
            if '' in a:
                a.remove('')
        if len(a) < 9:
            print("{} smaller".format(index))
            companies_data = companies_data.drop(companies_data.index[index])
        elif len(a) > 9:
            print("{} larger".format(index))
            companies_data = companies_data.drop(companies_data.index[index])
        else:
            the_row.append(row[1]) # cui
            the_row.append(a[1]) # year
            the_row.append(a[2]) # cifra de afaceri
            the_row.append(a[3]) # profit net
            the_row.append(a[4]) # datorii
            the_row.append(a[5]) # act_imob
            the_row.append(a[6]) # act_cirt
            the_row.append(a[7]) # cap
            the_row.append(a[8]) # angajati
            financial_data.loc[len(financial_data)] = the_row
# %%
export_to_sql(financial_data, 'FinancialData')




# %%
fin_data = pd.read_excel('fin_data_xlsx.xlsx')
# %%
removehyph = lambda x: str(x).split("-")[-1]
removfspace = lambda x: str(x).split(" ")[-1]
removlspace = lambda x: str(x).split(" ")[1]
#%%
fin_data.cui = fin_data.cui.apply(removehyph)

#%%
fin_data.angajati = fin_data.angajati.apply(removfspace)
fin_data.angajati = fin_data.angajati.apply(removfspace)

fin_data.cifra_afaceri = fin_data.cifra_afaceri.apply(removfspace)
fin_data.cifra_afaceri = fin_data.cifra_afaceri.apply(removfspace)

fin_data.profit_net = fin_data.profit_net.apply(removfspace)
fin_data.profit_net = fin_data.profit_net.apply(removfspace)

fin_data.datorii = fin_data.datorii.apply(removfspace)
fin_data.datorii = fin_data.datorii.apply(removfspace)

fin_data.act_imob = fin_data.act_imob.apply(removfspace)
fin_data.act_imob = fin_data.act_imob.apply(removfspace)

fin_data.act_circ = fin_data.act_circ.apply(removfspace)
fin_data.act_circ = fin_data.act_circ.apply(removfspace)

fin_data.cap = fin_data.cap.apply(removfspace)
fin_data.cap = fin_data.cap.apply(removfspace)
# %%
fin_data.to_excel("fin_data_Clean.xlsx")
# %%
