# Archivo: etl_tools.py
import os
import zipfile
import polars as pl
import pandas as pd
import pyreadstat
import tempfile
import io
import shutil

def zips_a_parquet(ruta_origen, ruta_destino, columnas_necesarias, cols_texto, cols_numero):
    """
    Convierte Zips de Stata a Parquet.
    - Arregla automáticamente la fecha (YYMM -> ANIO, MES).
    - Fuerza tipos de datos estrictos.
    """
    
    if os.path.exists(ruta_destino):
        shutil.rmtree(ruta_destino)
    os.makedirs(ruta_destino, exist_ok=True)
    
    contador = 0
    print(f"--- Procesando desde: {ruta_origen} ---")

    for nombre_zip in os.listdir(ruta_origen):
        if not nombre_zip.lower().endswith('.zip'): continue
        
        ruta_zip = os.path.join(ruta_origen, nombre_zip)
        
        try:
            with zipfile.ZipFile(ruta_zip, 'r') as z:
                
                def procesar_interno(zip_obj, ruta_padre):
                    nonlocal contador
                    
                    for archivo in zip_obj.namelist():
                        if archivo.lower().endswith('.dta') and '__MACOSX' not in archivo:
                            print(f"   -> Archivo: {archivo} ...", end="\r")
                            tmp_path = None
                            try:
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.dta') as tmp:
                                    tmp.write(zip_obj.read(archivo))
                                    tmp_path = tmp.name
                                
                                # 1. Leer archivo Stata
                                try:
                                    df, meta = pyreadstat.read_dta(tmp_path, usecols=columnas_necesarias)
                                except:
                                    df, meta = pyreadstat.read_dta(tmp_path)

                                # 2. Pasar a Polars y Normalizar nombres
                                ldf = pl.from_pandas(df)
                                ldf = ldf.select([pl.col(c).alias(c.strip().upper()) for c in ldf.columns])
                                
                                # 3. LIMPIEZA DE TIPOS (Texto y Números)
                                for col in ldf.columns:
                                    if col in cols_texto:
                                        ldf = ldf.with_columns(pl.col(col).cast(pl.String))
                                    elif col in cols_numero:
                                        ldf = ldf.with_columns(
                                            pl.col(col).cast(pl.String)
                                            .str.replace(",", ".")
                                            .cast(pl.Float64, strict=False)
                                        )

                                # 4. INGENIERÍA DE FECHA (La corrección automática)
                                # Si existe la columna FECH, creamos ANIO y MES automáticos
                                if "FECH" in ldf.columns:
                                    ldf = ldf.with_columns([
                                        # Asegurar formato 4 dígitos (509 -> 0509)
                                        pl.col("FECH").cast(pl.String).str.pad_start(4, "0").alias("FECH_CLEAN")
                                    ]).with_columns([
                                        # Crear Año: "20" + "21" = "2021"
                                        (pl.lit("20") + pl.col("FECH_CLEAN").str.slice(0, 2)).alias("ANIO"),
                                        # Crear Mes: "09"
                                        pl.col("FECH_CLEAN").str.slice(2, 2).alias("MES")
                                    ]).drop("FECH_CLEAN") # Borramos la temporal

                                # 5. Guardar
                                ldf.write_parquet(os.path.join(ruta_destino, f"data_{contador}.parquet"))
                                contador += 1
                                
                            except Exception as e:
                                print(f"\n[Error] {archivo}: {e}")
                            finally:
                                if tmp_path and os.path.exists(tmp_path): os.remove(tmp_path)

                        elif archivo.lower().endswith('.zip'):
                            try:
                                z_bytes = io.BytesIO(zip_obj.read(archivo))
                                with zipfile.ZipFile(z_bytes) as z_anidado:
                                    procesar_interno(z_anidado, f"{ruta_padre}/{archivo}")
                            except: pass 

                procesar_interno(z, nombre_zip)
                
        except zipfile.BadZipFile:
            print(f"ZIP Corrupto: {nombre_zip}")

    print(f"\n¡Listo! {contador} archivos generados en {ruta_destino}")