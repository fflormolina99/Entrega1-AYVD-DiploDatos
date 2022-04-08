#Para este punto elegi como variables numericas al salario neto y a los años de antiguedad, y como variable categórica al género. El objetivo es ver como
#se relacionan los años de antiguedad con el salario y ver si, como se espera, los varones ganan mas que las mujeres para la misma antiguedad, ya que 
#al hablar de comparar salarios, la antiguedad es un factor importante. Grafique ademas en el scatterplot el salario promedio para cada valor de antiguedad
#de forma de tener un buen criterio para distinguir salarios altos de bajos con solo mirar el gráfico.

#Importo los paquetes que necesito
import io
import matplotlib
import matplotlib.pyplot as plt
import numpy
import pandas as pd
import seaborn

#Le pido a seaborn que tenga un formato para charla (talk) y le pido a pandas que me de todo con dos decimales de precision
seaborn.set_context('talk')
pd.set_option("display.precision", 2)

#Cargo los datos al dataframe
url = 'https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/sysarmy_survey_2020_processed.csv'
df = pd.read_csv(url)

#Filtro los salarios menores al salario minimo de 2020
dff = df[df['salary_monthly_NETO']>20000]
print(dff['salary_monthly_NETO'].min())

#Aca le pido que me ordene los valores de la columna de antiguedad en orden ascendente
data=dff.sort_values(by='work_years_in_company', ascending=True)
data.head()

#Agrupo los datos de acuerdo a la antiguedad y le pido que me haga estadistica en la columnda del salario neto, para saber mas o menos que 
#valores manejamos
data.groupby(['work_years_in_company'])['salary_monthly_NETO'].describe()

#Aca me defino una lista en la que cada entrada es el promedio del salario neto para cada año de antiguedad en orden ascendente
mean = data.groupby(['work_years_in_company'])['salary_monthly_NETO'].mean()
print(mean)
print(len(mean))
print(type(mean))

#Ahora me quiero hacer una lista de los valores que se obtuvieron en la encuesta para años de antiguedad en orden ascendente. Paso los valores
#de la columna a una lista
yearss=data['work_years_in_company'].tolist()
print(yearss)

#Como no me interesan los valores repetidos, convierto la lista a un conjunto, para que se eliminen los datos repetidos
years2 = set(yearss)
print(years2)

#Convierto de nuevo el conjunto a lista
years_=list(years2)
print(years_)

#Ordeno los valores en orden ascendente
years = sorted(years_)
print(years)

#Aca grafico todo. Uso hue en seaborn.scatterplot para que me grafique los años de antiguedad en funcion del salario neto discriminando por genero
#Ademas uso las listas que me fabrique antes del dataframe para que me grafique los salarios promedio para cada valor distinto de antiguedad, de forma
#de ver mejor a partir de que punto podemos decir que un salario es alto o bajo
seaborn.set_context('talk',font_scale=0.6,rc={'figure.figsize':(10.0,15.0)})
plt.figure(figsize=(18,8))
plt.xlabel('Salario neto')
plt.ylabel('Años de antigüedad')
plt.plot(mean,years,linewidth=1.,linestyle='--',label='Salario promedio',color='magenta')
seaborn.scatterplot(data=dff,x='salary_monthly_NETO',y='work_years_in_company',hue='profile_gender')

#En esta parte restrinjo los datos a los salarios menores a $500000, porque en el grafico anterior se ve que la densidad es muchisimo mayor 
#en esos valores de salario que para salarios mas altos. LO hago para distinguir mejor la dispersion de datos en esa zona donde estan todos "amuchados"
dfr = dff[dff['salary_monthly_NETO']<500000]
seaborn.set_context('talk',font_scale=0.6,rc={'figure.figsize':(10.0,15.0)})
plt.figure(figsize=(18,8))
plt.xlabel('Salario neto')
plt.ylabel('Años de antigüedad')
plt.plot(mean,years,linewidth=1.5,linestyle='--',label='Salario promedio',color='magenta')
seaborn.scatterplot(data=dfr,x='salary_monthly_NETO',y='work_years_in_company',hue='profile_gender')
