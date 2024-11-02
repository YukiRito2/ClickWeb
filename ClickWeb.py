from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configura el servicio de ChromeDriver con la ruta de tu controlador
service = Service("C:\\SeleniumDrivers\\chromedriver-win64\\chromedriver.exe")

# URL de la página de votación
url = "https://limakid.com/modelkid/1119871/?mlang=es"

# Configura las opciones de Chrome para abrir en modo incógnito y otras opciones
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-logging")

# Abre el navegador en modo incógnito con dos pestañas
driver = webdriver.Chrome(service=service, options=chrome_options)
actions = ActionChains(driver)
wait = WebDriverWait(driver, 3)  # Espera explícita de hasta 10 segundos

# Abre dos pestañas
driver.get(url)
driver.execute_script("window.open('');")  # Abre una segunda pestaña en blanco

# Selecciona la primera pestaña para iniciar la votación
driver.switch_to.window(driver.window_handles[0])

# Bucle para repetir el proceso de votación
while True:
    try:
        # Carga la página principal de votación en la primera pestaña
        driver.get(url)
        time.sleep(3)  # Espera que cargue completamente

        # Variable de control para verificar los pasos
        votacion_exitosa = False

        # Paso 1: Hacer clic en el botón "VOTAR"
        votar_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='shadow bmessenger muy_grande' and contains(text(), 'VOTAR')]",
                )
            )
        )
        actions.move_to_element(votar_button).click().perform()
        time.sleep(3)

        # Intentar cerrar el anuncio con el SVG de "X"
        try:
            cerrar_anuncio = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//svg[@viewBox='0 0 48 48']"))
            )
            cerrar_anuncio.click()
            time.sleep(1)
            print("Anuncio encontrado y cerrado.")
        except:
            print(
                "No se encontró el botón de cierre del anuncio. Continuando con el proceso de votación."
            )

        # Paso 2: Hacer clic en el botón "Sí. Votar"
        confirmar_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'logButton') and contains(text(), 'Sí. Votar')]",
                )
            )
        )
        actions.move_to_element(confirmar_button).click().perform()
        time.sleep(2)  # Espera para que el voto se registre

        # Si ambos pasos se completan sin errores, marcamos como exitosa la votación
        votacion_exitosa = True

        # Paso 3: Solo hacer clic en "Ver resultados" si los pasos anteriores fueron exitosos
        if votacion_exitosa:
            ver_resultados_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(@class, 'logButton') and contains(text(), 'Ver resultados')]",
                    )
                )
            )
            actions.move_to_element(ver_resultados_button).click().perform()
            time.sleep(8)  # Espera para que los resultados se muestren

        # Cerrar la pestaña actual y abrir una nueva para continuar votando
        driver.close()
        driver.switch_to.window(
            driver.window_handles[0]
        )  # Cambiar a la otra pestaña que queda abierta
        driver.execute_script("window.open('');")  # Abre una nueva pestaña en blanco
        driver.switch_to.window(
            driver.window_handles[-1]
        )  # Cambia a la nueva pestaña para el próximo ciclo

    except Exception as e:
        print("Error en el proceso de votación:", e)

    # Pausa antes de reiniciar el ciclo para evitar sobrecarga en el servidor
    time.sleep(3)
