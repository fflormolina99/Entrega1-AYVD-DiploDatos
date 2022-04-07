# Importamos las librerías

import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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

# Filtrando valores extremos y erroneos

# Se eliminan los valores extremos de la variable 
# salary_monthly_NETO para filtrar errores
min_salary = df.salary_monthly_NETO.quantile(0.05)
max_salary = df.salary_monthly_NETO.quantile(0.95)

filter = df[(df['salary_monthly_NETO'] > min_salary) & (df['salary_monthly_NETO'] < max_salary)]

filter = filter[filter['tools_programming_languages'] != 'Ninguno']

# Análisis de la distribución de sueldos

mean_smn = np.mean(filter.salary_monthly_NETO)
median_smn = np.median(filter.salary_monthly_NETO)

df_clean_rec_mean = filter[filter.salary_monthly_NETO > mean_smn]
df_clean_rec_median = filter[filter.salary_monthly_NETO > median_smn]

nrows = 2
ncols = 3
figure1, axes = plt.subplots(nrows, ncols, figsize=(18, 9))
ax11, ax12, ax13, ax21, ax22, ax23 = axes.flatten()

seaborn.histplot(df_clean_rec_mean['salary_monthly_NETO'], bins=10, ax=ax11,
                stat='count', color='gray')  # histograma con 10 bins-.
ax11.axvline(df_clean_rec_mean['salary_monthly_NETO'].mean(),
                color='orangered', linestyle='--', label='Media')
ax11.axvline(df_clean_rec_mean['salary_monthly_NETO'].median(),
                color='indigo', linestyle='-.', label='Mediana')
seaborn.histplot(df_clean_rec_mean['salary_monthly_NETO'], bins=50, ax=ax12,
                stat='count', color='gray')  # histograma con 50 bins-.
ax12.axvline(df_clean_rec_mean['salary_monthly_NETO'].mean(),
                color='orangered', linestyle='--', label='Media')
ax12.axvline(df_clean_rec_mean['salary_monthly_NETO'].median(),
                color='indigo', linestyle='-.', label='Mediana')
seaborn.histplot(df_clean_rec_mean['salary_monthly_NETO'], bins=100, ax=ax13,
                stat='count', color='gray')  # Histograma con 100 bins)
ax13.axvline(df_clean_rec_mean['salary_monthly_NETO'].mean(),
                color='orangered', linestyle='--', label='Media')
ax13.axvline(df_clean_rec_mean['salary_monthly_NETO'].median(),
                color='indigo', linestyle='-.', label='Mediana')

seaborn.histplot(df_clean_rec_median['salary_monthly_NETO'], bins=10, ax=ax21,
                stat='count', color='gray')  # Histograma con 10 bins-.
ax21.axvline(df_clean_rec_median['salary_monthly_NETO'].mean(),
                color='orangered', linestyle='--', label='Media')
ax21.axvline(df_clean_rec_median['salary_monthly_NETO'].median(),
                color='indigo', linestyle='-.', label='Mediana')
seaborn.histplot(df_clean_rec_median['salary_monthly_NETO'], bins=50, ax=ax22,
                stat='count', color='gray')  # Histograma con 50 bins-.
ax22.axvline(df_clean_rec_median['salary_monthly_NETO'].mean(),
                color='orangered', linestyle='--', label='Media')
ax22.axvline(df_clean_rec_median['salary_monthly_NETO'].median(),
                color='indigo', linestyle='-.', label='Mediana')
seaborn.histplot(df_clean_rec_median['salary_monthly_NETO'], bins=100, ax=ax23,
                stat='count', color='gray') # histograma con 100 bins-.
ax23.axvline(df_clean_rec_median['salary_monthly_NETO'].mean(),
                color='orangered', linestyle='--', label='Media')
ax23.axvline(df_clean_rec_median['salary_monthly_NETO'].median(),
                color='indigo', linestyle='-.', label='Mediana')

ax11.legend()
ax12.legend()
ax13.legend()
ax21.legend()
ax22.legend()
ax23.legend()

ax11.grid()
ax12.grid()
ax13.grid()
ax21.grid()
ax22.grid()
ax23.grid()

seaborn.despine()

plt.show()
# CONCLUSION: al comparar la grafica obtenida con el PDF original y el PDF
# editado se ve como influyen los valores pequenos y grandes, tienden a
# llevar la media y la mediana hacia menores valores, la forma  de la
# distribucion es imperceptible y, aun habiendo eliminado los sueldos
# grandes (correspondientes solo al 5% de los datos), la media es mayor
# que la mediana, lo cual nos dice que la distribucion tiene una cola
# hacia valores grandes y no se corresponde a una distribucion normal.

# Crear una columna nueva con la lista de lenguajes en lugar de un string
filter.loc[:, 'cured_programming_languages'] = filter.tools_programming_languages\
    .apply(split_languages)

# Se seleccionan los top 99 conjuntos de lenguajes más populares
language_count = filter.cured_programming_languages.value_counts()\
    .reset_index()\
    .rename(columns={'index': 'language', 'cured_programming_languages': 'frequency'})

language_count = language_count[language_count['language'].astype(bool)]

language_count = language_count[language_count['frequency'] > language_count.frequency.quantile(0.99)]

freq_list = language_count['language'].to_list()
print(freq_list)
filter_top = filter[filter['cured_programming_languages'].isin(freq_list)].reset_index()

# Filtrado extra
filter_top['tools_programming_languages'] = filter_top['tools_programming_languages'].replace('Python, Sql', 'Python, SQL').replace('SQL, Ninguno de los anteriores', 'SQL')

# Plot
# Se grafícan los lenguajes más valorados económicamente dentro del top.

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
#  - Para casi todos los lenguajes se cumple que la media es mayor a la mediana. Esto nos indica que la curva que desriben estos datos tiene su pico por debajo de la media. Una gran dispersión por lo tanto, nos va a indicar que se trata de una curva más suave y por lo tanto con mayor posibilidad de obtener un salario elevado.
#  - Python aparece 4 veces en el top 50% de lenguajes populares mejores pagos dentro de los más populares.
#  - Los stacks de lenguajes relacionados a al análisis de datos (Python, SQL y bash) están todos dentro del top de los lenguajes más populares y mejores pagos.
#  - Los stacks de desarrollo front end si bien tienen mucha más frecuencia, están en la mitad inferior del orden por salarios.
