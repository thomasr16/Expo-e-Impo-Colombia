# src/viz_tools.py - Tools de visualización con Plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def graficar_linea_tiempo(df, x_col, y_col, titulo, color_col=None):
    """Genera un gráfico de línea temporal."""
    fig = px.line(
        df, x=x_col, y=y_col, color=color_col,
        title=titulo, markers=True, template="plotly_white"
    )
    fig.update_layout(yaxis_title="Valor (USD)", xaxis_title="Año")
    return fig

def graficar_balanza_comercial(df_agrupado):
    """
    Gráfico específico para Balanza Comercial:
    Muestra Impo y Expo como barras y el saldo como línea.
    """
    # df_agrupado debe tener columnas: ANIO, TIPO, VALOR
    
    fig = px.bar(
        df_agrupado, x="ANIO", y="VALOR", color="TIPO",
        barmode="group", title="Balanza Comercial: Importaciones vs Exportaciones",
        color_discrete_map={"Importación": "#EF553B", "Exportación": "#636EFA"},
        template="plotly_white"
    )
    return fig

def graficar_treemap_productos(df, path_cols, value_col, titulo):
    """
    Mapa de árbol para ver jerarquía de productos (Capítulos -> Partidas).
    """
    fig = px.treemap(
        df, path=path_cols, values=value_col,
        title=titulo, color=value_col, color_continuous_scale='Blugrn'
    )
    return fig
def graficar_saldo_paises(df, top_n=20):
    """
    Muestra un gráfico de barras divergentes.
    Barras a la derecha (Verdes) = Superávit (Ganamos).
    Barras a la izquierda (Rojas) = Déficit (Perdemos).
    
    Espera un DF con columnas: ['PAIS', 'SALDO']
    """
    # 1. Ordenamos por Saldo para que el gráfico se vea escalonado
    df_sorted = df.sort_values(by="SALDO", ascending=True)
    
    # Filtramos solo los Top N (los que más ganamos y los que más perdemos)
    # Tomamos los N primeros (déficit) y N últimos (superávit) si el df es muy grande
    if len(df_sorted) > top_n:
        df_plot = pd.concat([df_sorted.head(top_n//2), df_sorted.tail(top_n//2)])
    else:
        df_plot = df_sorted

    # 2. Definimos color basado en si es ganancia o pérdida
    df_plot['RESULTADO'] = df_plot['SALDO'].apply(lambda x: 'Superávit (Ganamos)' if x > 0 else 'Déficit (Perdemos)')
    
    color_map = {'Superávit (Ganamos)': '#2ECC71', 'Déficit (Perdemos)': '#E74C3C'}

    fig = px.bar(
        df_plot, 
        y="PAIS", 
        x="SALDO", 
        color="RESULTADO",
        title=f"Balanza Comercial: Países con mayor Déficit y Superávit",
        orientation='h', # Barras horizontales
        color_discrete_map=color_map,
        template="plotly_white",
        text_auto='.2s' # Muestra el valor resumido (ej. 2M, 1k)
    )
    
    fig.update_layout(xaxis_title="Saldo en USD (Exportaciones - Importaciones)")
    return fig

def graficar_saldo_sectores(df, sector_col="CODIGO", top_n=15):
    """
    Muestra en qué sectores de la economía ganamos más dinero neto.
    Espera un DF con: ['CODIGO', 'SALDO', 'NOMBRE_SECTOR' (opcional)]
    """
    df_sorted = df.sort_values(by="SALDO", ascending=False).head(top_n)
    
    fig = px.bar(
        df_sorted,
        x="CODIGO",
        y="SALDO",
        title=f"Top {top_n} Sectores/Capítulos donde más ganamos (Superávit)",
        color="SALDO",
        color_continuous_scale="Blugrn", # Escala de verdes/azules
        template="plotly_white"
    )
    return fig

def graficar_variacion_pct(df, tipo_flujo="Exportación", top_n=10):
    """
    Gráfico de barras divergentes para variación porcentual.
    """
    # Ordenamos por %
    df_sorted = df.sort_values(by="VARIACION_PCT", ascending=True)
    df_plot = pd.concat([df_sorted.head(top_n), df_sorted.tail(top_n)])

    df_plot['ESTADO'] = df_plot['VARIACION_PCT'].apply(lambda x: 'Crecimiento' if x > 0 else 'Caída')

    fig = px.bar(
        df_plot,
        x="VARIACION_PCT",
        y="CODIGO",
        color="ESTADO",
        orientation='h',
        title=f"Top Sectores por Variacion Porcentual (%) en {tipo_flujo}",
        color_discrete_map={'Crecimiento': '#2ECC71', 'Caída': '#E74C3C'},
        template="plotly_white",
        text_auto='.1f' # Muestra un decimal
    )

    fig.update_layout(
        xaxis_title="Variación Porcentual (%)",
        yaxis_title="Sector",
        xaxis=dict(ticksuffix="%")
    )
    return fig