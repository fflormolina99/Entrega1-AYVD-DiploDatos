# Importamos las librerías

import io
import matplotlib
import matplotlib.pyplot as plt
import numpy
import pandas as pd
import seaborn

seaborn.set_context('talk')

###
### FUNCIONES
###

# Convert the comma-separated string of languages to a list of string.
# Remove 'ninguno de los anteriores' option, spaces and training commas.
def split_languages(languages_str):
  if not isinstance(languages_str, str):
    return []
  # Remove 'other' option
  languages_str = languages_str.lower()\
    .replace('ninguno de los anteriores', '')
  # Split string into list of items
  # Remove spaces and commas for each item
  return [lang.strip().replace(',', '')
          for lang in languages_str.split()]



# Lectura del dataset

url = 'https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/sysarmy_survey_2020_processed.csv'
df = pd.read_csv(url)

# Seteando las columnas relevantes

relevant_columns = ['tools_programming_languages', 'salary_monthly_NETO']

# Filtrando valores extremos y erroneos

filter = df[df['salary_monthly_NETO'] > 20000]
filter = filter[filter['salary_monthly_NETO'] < 1000000]
filter = filter[filter['tools_programming_languages'] != 'Ninguno']

# Crear una columna nueva con la lista de lenguajes en lugar de un string
filter.loc[:, 'cured_programming_languages'] = filter.tools_programming_languages\
    .apply(split_languages)
if 'cured_programming_languages' not in relevant_columns:
    relevant_columns.append('cured_programming_languages') 


# Duplicate each row of df for each programming language
# mentioned in the response.
# We only include in df_lang the columns we are going to analyze later, so we
# don't duplicate innecesary information.

# df_lang = filter.cured_programming_languages\
#     .apply(pd.Series).stack()\
#     .reset_index(level=-1, drop=True).to_frame()\
#     .join(filter[relevant_columns])\
#     .rename(columns={0: 'programming_language'})

language_count = filter.cured_programming_languages.value_counts()\
    .reset_index()\
    .rename(columns={'index': 'language', 'cured_programming_languages': 'frequency'})
freq_list = language_count['language'][:11].to_list()
freq_list = [x for x in freq_list if x] # Elimino unos elementos vacíos 

filter_top = filter[filter['cured_programming_languages'].isin(freq_list)].reset_index()

# Plot

plt.figure(figsize=(12, 6))
seaborn.boxplot(data=filter_top, x='salary_monthly_NETO', y='tools_programming_languages',
                color='orangered')
plt.ticklabel_format(style='plain', axis='x')
