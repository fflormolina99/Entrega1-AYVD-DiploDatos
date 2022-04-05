# Si, existe una correlación lineal entre las columnas Salario Bruto y Neto. Se propone eliminar de la encuesta la columna de Salario Bruto para que la encuesta sea mas simple.
# Se utiliza el coeficiente de Pearson para determinar la correlación. Esté tiene un valor de 0,83 lo que indica una alta correlación positiva entre las columnas.

#  Crear subconjunto de df.
df_s = df[["salary_monthly_BRUTO","salary_monthly_NETO"]]
df_s.head()

# Eliminar Nan
df_s = df_s.dropna(how='all')

# Coeficiente de Pearson
df_s["salary_monthly_BRUTO"].corr(df_s["salary_monthly_NETO"])

import matplotlib.pyplot as plt

plt.plot(df_s["salary_monthly_BRUTO"], df_s["salary_monthly_NETO"],"ro")
plt.title("Correlación Salario Bruto vs Salario Neto")