import pandas as pd

# --- CAPA DE DATOS (Configuración inicial) ---
def cargar_datos(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
        return None

# --- CAPA DE LÓGICA (Funciones de análisis) ---

def analizar_reprobacion(df):
    print("\n--- [1] MATERIAS CON MAYOR ÍNDICE DE REPROBACIÓN ---")
    df['reprobado'] = df['calificacion'] < 6.0
    indice = (df.groupby('materia')['reprobado'].mean() * 100).sort_values(ascending=False)
    print(indice.head(10).apply(lambda x: f"{x:.2f}%"))

def analizar_carreras(df):
    print("\n--- [2] CARRERAS CON MAYOR PROMEDIO ---")
    promedio = df.groupby('carrera')['calificacion'].mean().sort_values(ascending=False)
    print(promedio.apply(lambda x: f"{x:.2f}"))

def analizar_tendencias(df):
    print("\n--- [3] TENDENCIAS POR SEMESTRE (PROMEDIO) ---")
    tendencia = df.groupby('semestre')['calificacion'].mean()
    print(tendencia.to_string())

def analizar_riesgos(df):
    print("\n--- [4] POSIBLES RIESGOS ACADÉMICOS ---")
    df['reprobado'] = df['calificacion'] < 6.0
    est_metrics = df.groupby('id_estudiante').agg({'calificacion': 'mean', 'reprobado': 'sum'})
    riesgos = est_metrics[(est_metrics['calificacion'] < 6.0) | (est_metrics['reprobado'] >= 2)]
    print(f"Estudiantes en riesgo detectados: {len(riesgos)}")
    print(riesgos.head(10))

# --- CAPA DE INTERFAZ (Menú por Terminal) ---

def menu():
    df = cargar_datos('datos_rendimiento_universidad.csv')
    if df is None: return

    while True:
        print("\n" + "="*40)
        print("SISTEMA DE ANÁLISIS ACADÉMICO (V2.0)")
        print("="*40)
        print("1. Materias con más reprobados")
        print("2. Carreras con mejor promedio")
        print("3. Tendencias por semestre")
        print("4. Detección de riesgos")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción (1-5): ")

        match opcion:
            case "1": analizar_reprobacion(df)
            case "2": analizar_carreras(df)
            case "3": analizar_tendencias(df)
            case "4": analizar_riesgos(df)
            case "5": 
                print("Cerrando sistema...")
                break
            case _: 
                print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()