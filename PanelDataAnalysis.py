# -*- coding: utf-8 -*-
"""ProjektZaliczeniowyEDP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l28Eq_4RwgzSE10PmezzHv0tcvnLVYw-

# wstępna analiza danych
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Wczytaj dane z pliku CSV
df = pd.read_csv('PanelData.csv')

"""## Sprawdzenie braków danych"""

df = pd.read_csv('PanelData.csv')

# Sprawdzamy, czy w danych występują braki
braki_danych = df.isnull().any()

# Wyświetlamy wyniki
print(braki_danych)

"""wszystkie wartości są False, to oznacza, że w danych nie ma braków. Jeśli którakolwiek z wartości byłaby True, to oznaczałoby to, że istnieją braki danych w odpowiadającej kolumnie."""

# Wykluczamy kolumny 'I' oraz 'T' z analizy
columns_to_exclude = ['I', 'T']
df_filtered = df.drop(columns=columns_to_exclude)

# Wyświetlamy kilka pierwszych wierszy danych
print("Pierwsze 5 wierszy danych:")
print(df_filtered.head())

# Wyświetlamy podstawowe statystyki opisowe
print("\nPodstawowe statystyki opisowe:")
print(df_filtered.describe())

"""## Macierz korelacji"""

# Obliczamy korelację między kolumnami w tym zmienna objasniana
correlation_matrix = df_filtered.corr()

print("\nMacierz korelacji:")
print(df_filtered.corr())

# Heatmapa
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Heatmap Macierzy Korelacji - wszystkie zmienne w tym objasniana')
plt.show()



#wykluczenie zmiennej objasniającej C
columns_to_exclude = ['C','I', 'T']
df_filtered = df.drop(columns=columns_to_exclude)


# Obliczamy korelację między kolumnami tylko zmienne objasniane
correlation_matrix = df_filtered.corr()

print("\nMacierz korelacji:")
print(df_filtered.corr())

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Heatmap Macierzy Korelacji - tylko zmienne objasniające')
plt.show()

"""## Wykresy szeregów panelu"""

for column in df_filtered.columns:
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='T', y=column, hue='I', data=df)
    plt.title(f'Wykres szeregów panelu dla zmiennej {column}')
    plt.xlabel('Rok (T)')
    plt.ylabel(column)
    plt.legend(title='Przekrój (I)')
    plt.show()

"""## Weryfikacja rozrzutu danych"""

# Tworzymy osobne wykresy rozrzutu dla kolumn Q i PF
plt.figure(figsize=(12, 6))

# Wykres dla kolumny Q
plt.subplot(1, 2, 1)
sns.scatterplot(x=df['C'], y=df['Q'], color='blue')
plt.title('Wykres rozrzutu dla kolumny Q')
plt.xlabel('Wartość Y')

# Wykres dla kolumny PF
plt.subplot(1, 2, 2)
sns.scatterplot(x=df['C'], y=df['PF'], color='green')
plt.title('Wykres rozrzutu dla kolumny PF')
plt.xlabel('Wartość Y')

plt.tight_layout()
plt.show()

"""Sprawdzamy to samo dla logarytmów kolumn"""

# kolumny C oraz PF jako logarytmy
df_log =df.copy()
df_log['logQ'] = np.log(df['Q'])
df_log['logPF'] = np.log(df['PF'])
df_log.drop('Q',
  axis='columns', inplace=True)
df_log.drop('PF',
  axis='columns', inplace=True)

# Tworzymy osobne wykresy rozrzutu dla logarytmów kolumn Q i PF na osi X oraz C na osi Y
plt.figure(figsize=(12, 6))

# Wykres dla logarytmu kolumny Q
plt.subplot(1, 2, 1)
sns.scatterplot(x=df_log['logQ'], y=df_log['C'], color='blue')
plt.title('Wykres rozrzutu dla logarytmu kolumny Q')
plt.xlabel('logQ')

# Wykres dla logarytmu kolumny PF
plt.subplot(1, 2, 2)
sns.scatterplot(x=df_log['logPF'], y=df_log['C'], color='green')
plt.title('Wykres rozrzutu dla logarytmu kolumny PF')
plt.xlabel('logPF')

plt.tight_layout()
plt.show()

"""# Wybór postaci modelu

## Model Regresji Łącznej
"""

# Dodanie stałej do danych
df['const'] = 1

# Zdefiniowanie zmiennych niezależnych
X = df[['const', 'PF', 'LF', 'Q']]

# Zdefiniowanie zmiennej zależnej
y = df['C']

# Dopasowanie modelu regresji łącznej
MRL = sm.OLS(y, X).fit()

# Wypisanie podsumowania modelu
print(MRL.summary())

print(MRL.params)

# Dodanie stałej do danych
df_log['const'] = 1

# Zdefiniowanie zmiennych niezależnych
X = df_log[['const', 'logPF', 'LF', 'logQ']]

# Zdefiniowanie zmiennej zależnej
y = df['C']

# Dopasowanie modelu regresji łącznej
MRL = sm.OLS(y, X).fit()

# Wypisanie podsumowania modelu
print(MRL.summary())

"""## Model FE jednokierunkowy"""

df_copy = df.copy()

# Ustawienie MultiIndex na podstawie zmiennych 'I' i 'T'
df_copy.set_index(['I', 'T'], inplace=True)

# Dodanie stałej do zmiennych
df_copy['const'] = 1


y = df_copy['C']


exog_vars = ['const', 'PF', 'LF', 'Q']

#tworzenie modelu
model_fe = PanelOLS(y, df_copy[exog_vars], entity_effects=True)

results_fe = model_fe.fit()

print(results_fe)

df_copy = df.copy()

# Ustawienie MultiIndex na podstawie zmiennych 'I' i 'T'
df_copy.set_index(['I', 'T'], inplace=True)

df_copy['const'] = 1

y = df_copy['C']

exog_vars = ['const', 'PF', 'LF', 'Q']

# model efektów ustalonych jednokierunkowych (fixed effects)
model_fe_changed = PanelOLS(y, df_copy[exog_vars], entity_effects=True)

results_fe_changed = model_fe_changed.fit(cov_type='kernel', kernel='bartlett')

print(results_fe_changed)

# Test Durbina-Watsona
print("\nTest Durbina-Watsona:")
dw_statistic = durbin_watson(results_fe_changed.resids)
print(f"Durbin-Watson Statistic: {dw_statistic}")