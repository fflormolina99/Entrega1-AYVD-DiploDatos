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


# Se seleccionan los 10 conjuntos de lenguajes más populares
language_count = filter.cured_programming_languages.value_counts()\
    .reset_index()\
    .rename(columns={'index': 'language', 'cured_programming_languages': 'frequency'})

language_count = language_count[language_count['language'].astype(bool)]

freq_list = language_count['language'][:10].to_list()
print(freq_list)
filter_top = filter[filter['cured_programming_languages'].isin(freq_list)].reset_index()
filter_top['tools_programming_languages'] = filter_top['tools_programming_languages'].replace('Python, Sql', 'Python, SQL').replace('SQL, Ninguno de los anteriores', 'SQL')

# Plot
# Se grafícan los 10 grupos de lenguajes más valorados económicamente de la encuesta.

plt.figure(figsize=(12, 6))
seaborn.boxplot(data=filter_top, x='salary_monthly_NETO', y='tools_programming_languages',
                color='orangered')
plt.ticklabel_format(style='plain', axis='x')

# Se obtienen medidas del data set

selected_columns_top = filter_top.filter(items=['salary_monthly_NETO', 'tools_programming_languages'])
tmp = selected_columns_top.groupby(['tools_programming_languages']).mean().round(2).rename(columns={'salary_monthly_NETO': "Media"})
tmp.loc[:, 'Mediana'] = selected_columns_top.groupby(['tools_programming_languages']).median().round(2).salary_monthly_NETO
tmp.loc[:, 'Desviación std'] = selected_columns_top.groupby(['tools_programming_languages']).std().round(2).salary_monthly_NETO
tmp.sort_values(by='Media', ascending=False)

# En esta tabla se pueden ver distintas medidas de los datos en el data frame.
# Algunas conclusiones que se pueden sacar mirando solo estos valores, pueden ser:
#  - Para todos los lenguajes se cumple que la media es mayor a la mediana. Esto nos indica que la campana que desriben estos datos tiene su pico por debajo de la media. Una gran dispersión por lo tanto, nos va a indicar que se trata de una curva más plana y por lo tanto con mayor posibilidad de obtener un salario elevado.
#  - Python aparece 3 veces en el top 5 de lenguajes populares mejores pagos. 
#  - Se puede ver que los lenguajes como Python y Javascript solos, en conjunto con Java son lenguajes que se pueden utilizar en muchos tipos de proyectos, lo cual podría explicar la gran dispersión que tienen con respecto a los lenguajes de Bash y SQL que son de propositos específicos y tienen un sueldo mucho más estandarizado.
#  - También se puede ver que los stacks con más de un lenguaje tienen dispersiones mayores, lo cual va de acuerdo al punto anterior.
