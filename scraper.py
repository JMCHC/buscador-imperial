import os
import subprocess
from playwright.sync_api import sync_playwright
import pandas as pd

# Instalación automática de navegadores si no existen
subprocess.run(["playwright", "install", "chromium"])

def buscar_en_imperial(termino):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = f"https://www.imperial.cl/search?Ntt={termino.replace(' ', '%20')}&searchType=simple&Nrpp=36"
        page.goto(url)
        
        # Esperamos a que los elementos estén presentes
        page.wait_for_selector('.osf__sc-1d18s5c-5', timeout=20000)
        
        productos_lista = []
        items = page.query_selector_all('.osf__sc-1d18s5c-5')
        
        for item in items:
            nombre_el = item.query_selector('h2')
            precio_el = item.query_selector('.osf__sc-1d18s5c-16')
            if nombre_el and precio_el:
                productos_lista.append({
                    "Producto": nombre_el.inner_text().strip(), 
                    "Precio": precio_el.inner_text().strip()
                })
        
        browser.close()
        return pd.DataFrame(productos_lista)
