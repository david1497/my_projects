#%%
import pandas as pd

#%%
companies = pd.read_excel('C:\\Users\\citco\\Downloads\\Book1.xlsx')
# %%
remove_space = lambda x: str(x).replace(' ', '')
remove_slash = lambda x: str(x).replace('/', '')
remove_dash = lambda x: str(x).replace('-', '')
remove_Ldash = lambda x: str(x).replace('—', '')
replaceplus = lambda x: str(x).replace('+', '00')
get_country = lambda x: str(x).split('.')[-1].split('/')[0]
companies['phone'] = companies['phone'].apply(remove_space)
companies['phone'] = companies['phone'].apply(remove_slash)
companies['phone'] = companies['phone'].apply(remove_dash)
companies['phone'] = companies['phone'].apply(remove_dash)
companies['phone'] = companies['phone'].apply(replaceplus)
companies['countrycode'] = companies['website'].apply(get_country)
# %%
companies.to_excel('step1_data_cleaned.xlsx')

# %%
remove_first_space = lambda x: str(x)[1:]
replaceleft = lambda x: str(x).replace('(', '')
replaceright = lambda x: str(x).replace(')', '')
replacedot = lambda x: str(x).replace('.', '')
cleaned_phone = pd.read_excel('step1_data_cleaned.xlsx')
cleaned_phone['phone'] = cleaned_phone['phone'].apply(remove_first_space)
cleaned_phone['phone'] = cleaned_phone['phone'].apply(replaceleft)
cleaned_phone['phone'] = cleaned_phone['phone'].apply(replaceright)
cleaned_phone['phone'] = cleaned_phone['phone'].apply(replacedot)
cleaned_phone['phone'] = cleaned_phone['phone'].apply(remove_space)
cleaned_phone['phone'] = cleaned_phone['phone'].apply(remove_slash)
cleaned_phone['phone'] = cleaned_phone['phone'].apply(remove_dash)
cleaned_phone['phone'] = cleaned_phone['phone'].apply(remove_Ldash)
cleaned_phone.to_excel('step2_data_cleaned.xlsx')
# %%
df = cleaned_phone.groupby(['phone']).size().reset_index(name='count')
# %%
cleaned_phone1 = cleaned_phone
cleaned_phone1.drop_duplicates(subset='phone', keep='last', inplace=True)
cleaned_phone1.to_excel('step3_data_cleaned.xlsx')
# %%
cleaned_phone2 = pd.read_excel('step3_data_cleaned.xlsx')
cleaned_phone2.drop_duplicates(subset=['name', 'phone'], keep='last', inplace=True)
cleaned_phone2.to_excel('step4_data_cleaned.xlsx')
# %%
at = lambda x: if(str(x)[0:3] == "049"): 