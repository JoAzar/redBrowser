from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEnginePage, QWebEngineView, QWebEngineSettings
import re
import os
import sys

class IncognitoWebEngineProfile(QWebEngineProfile):
    """Perfil de navegador en modo incógnito."""
    def __init__(self, name, parent=None):
        super().__init__(name, parent)  # Asegúrate de llamar al constructor de la clase base
        self.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        self.setPersistentStoragePath("")  # Usar un directorio vacío para almacenamiento persistente

class AdBlockingWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.load_filter_lists()

    def load_filter_lists(self):
        self.filters = []
        try:
            with open("filters/filtros.txt", "r") as f:
                self.filters = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("Archivo de filtros no encontrado.")

    def is_ad_request(self, url):
        return any(re.search(filter_pattern, url, re.IGNORECASE) for filter_pattern in self.filters)

    def createWindow(self, _type):
        new_page = AdBlockingWebEnginePage(self.profile(), self)
        return new_page

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Rutas de los iconos
        base_dir = os.path.dirname(__file__)
        back_icon_path = os.path.join(base_dir, 'icons', 'back.png')
        forward_icon_path = os.path.join(base_dir, 'icons', 'forward.png')
        browser_icon_path = os.path.join(base_dir, 'icons', 'iconoBrowser.ico')

        # Configurar perfil del navegador en modo incógnito
        self.profile = IncognitoWebEngineProfile("IncognitoProfile")

        # Configurar vista del navegador
        self.browser = QWebEngineView()
        self.browser.setPage(AdBlockingWebEnginePage(self.profile, self))
        
        # URL inicial
        ingreso = input("Ingrese su URL (sin https): ")
        self.browser.setUrl(QUrl("https://" + ingreso + ".com"))  # Convertir la URL a QUrl

        # Configurar barra de direcciones
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_url_bar)

        # Configurar botones de navegación
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(back_icon_path))
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon(forward_icon_path))
        self.forward_button.clicked.connect(self.browser.forward)

        # Aplicar estilo QSS
        self.apply_styles()

        # Configurar diseño
        self.layout = QVBoxLayout()
        self.url_layout = QHBoxLayout()
        self.url_layout.addWidget(self.back_button)
        self.url_layout.addWidget(self.forward_button)
        self.url_layout.addWidget(self.url_bar)
        self.layout.addLayout(self.url_layout)
        self.layout.addWidget(self.browser)

        # Configurar contenedor y ventana principal
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Configurar ícono de la ventana
        self.setWindowIcon(QIcon(browser_icon_path))
        self.setWindowTitle("Red Browser")
        self.resize(1024, 768)

        # Configurar opciones de privacidad
        self.configure_privacy_settings()

    def configure_privacy_settings(self):
        """Configura ajustes de privacidad en la vista del navegador."""
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)  # Desactivar JavaScript
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)  # Desactivar plugins
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)  # Desactivar almacenamiento local
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, False)  # Desactivar WebGL
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, False)  # Desactivar carga de imágenes
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled, False)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, False)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, False)
        settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, False)
        settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, False)
        settings.setAttribute(QWebEngineSettings.FocusOnNavigationEnabled, False)
        settings.setAttribute(QWebEngineSettings.PrintElementBackgrounds, False)
        settings.setAttribute(QWebEngineSettings.ShowScrollBars, True)
        settings.setAttribute(QWebEngineSettings.DnsPrefetchEnabled, True)
        settings.setAttribute(QWebEngineSettings.PdfViewerEnabled, False)

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))  # Convertir la URL a QUrl

    def update_url_bar(self, q):
        """Actualiza la barra de direcciones con la URL actual del navegador."""
        self.url_bar.setText(q.toString())

    def apply_styles(self):
        """Aplica estilos personalizados a los widgets."""
        self.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #888;
                padding: 5px;
                border-radius: 5px;
                min-width: 30px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #888;
                border-radius: 5px;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
