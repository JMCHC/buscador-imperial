from playwright.sync_api import sync_playwright
import pandas as pd

def buscar_en_imperial(termino):
    with sync_playwright() as p:
        # Abrimos navegador en modo headless (invisible)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Construcción del URL
        url = f"https://www.imperial.cl/search?Ntt={termino.replace(' ', '%20')}&searchType=simple&Nrpp=36"
        page.goto(url)
        
        # Esperamos a que los productos carguen
        page.wait_for_selector('.osf__sc-1d18s5c-5', timeout=10000)
        
        productos_lista = []
        # Seleccionamos los contenedores de los productos
        items = page.query_selector_all('.osf__sc-1d18s5c-5')
        
        for item in items:
            nombre_el = item.query_selector('h2')
            precio_el = item.query_selector('.osf__sc-1d18s5c-16')
            
            if nombre_el and precio_el:
                nombre = nombre_el.inner_text().strip()
                precio = precio_el.inner_text().strip()
                productos_lista.append({"Producto": nombre, "Precio": precio})
        
        browser.close()
        return pd.DataFrame(productos_lista)
