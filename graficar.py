import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":

    # Cargo archivo de resumen.txt con pandas delimitado con espacios en blanco   
    df = pd.read_csv("resumen.txt", sep='\s+', header=None)
    
    # Renombroi las columnas por indcorr, , ebest, epop, mingl, genmax
    df.columns = ['indcorr', 'ebest', 'epop', 'mingl', 'genmax']
    print(df.head(30))


    # Grafico la columna indcorr vs ebest
    plt.bar(df['indcorr'], df['ebest'], color='green')
    plt.title("Gráfica de indcorr vs ebest")
    plt.xlabel("indcorr")
    plt.ylabel("ebest")
    plt.show()  

    # Grafico la columna indcorr vs epop
    plt.bar(df['indcorr'], df['epop'], color='red')
    plt.title("Gráfica de indcorr vs epop")
    plt.xlabel("indcorr")
    plt.ylabel("epop")
    plt.show()

    # Grafico la columna indcorr vs mingl
    colores = ['red' if x != df['mingl'].min() else 'green' for x in df['mingl']]
    plt.bar(df['indcorr'], df['mingl'], color=colores)
    plt.title("Gráfica de indcorr vs mingl")
    plt.xlabel("indcorr")
    plt.ylabel("mingl")
    for i, v in enumerate(df['mingl']):
        plt.text(i, v + 0.5, str(v), ha='center', color='black')
    plt.show()

    # Grafico la columna indcorr vs genmax
    plt.bar(df['indcorr'], df['genmax'], color='orange')
    plt.title("Gráfica de indcorr vs genmax")
    plt.xlabel("indcorr")
    plt.ylabel("genmax")
    plt.show()

    # Grafico de dispersión de epop vs ebest
    plt.scatter(df['epop'], df['ebest'], color='blue')
    plt.title("Gráfica de dispersión de epop vs ebest")
    plt.xlabel("epop")
    plt.ylabel("ebest")
    plt.show()

    