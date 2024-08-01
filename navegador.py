from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEnginePage, QWebEngineView, QWebEngineSettings
import re

class IncognitoWebEngineProfile(QWebEngineProfile):
    """Clase personalizada para perfil de navegador en modo incógnito."""
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        # Configuración de cookies y almacenamiento persistente
        self.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        self.setPersistentStoragePath("")  # Usar un directorio vacío para almacenamiento persistente


class AdBlockingWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.network_access_manager = self.webPage().networkAccessManager()
        self.network_access_manager.finished.connect(self.on_request_finished)
        self.load_filter_lists()

    def load_filter_lists(self):
        self.filters = []
        # Cargar filtros desde un archivo o URL
        try:
            with open("/home/red/toolsR/filtros.txt", "r") as f:
                self.filters = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("Archivo de filtros no encontrado.")

    def is_ad_request(self, url):
        return any(re.search(filter_pattern, url, re.IGNORECASE) for filter_pattern in self.filters)

    def createWindow(self, _type):
        new_page = AdBlockingWebEnginePage(self.profile(), self)
        return new_page

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurar perfil del navegador en modo incógnito
        self.profile = IncognitoWebEngineProfile("IncognitoProfile", self)
        
        # Configurar vista del navegador
        self.browser = QWebEngineView()
        self.browser.setPage(QWebEnginePage(self.profile, self))
        ingreso = input("Ingrese su url (sin https): ")
        self.browser.setUrl(QUrl("https://"+ingreso))  # Convertir la URL a QUrl

        # Configurar opciones de privacidad
        self.configure_privacy_settings()

        # Configurar barra de direcciones
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_url_bar)

        # Configurar botones de navegación
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon("/home/red/toolsR/back.png"))
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon("/home/red/toolsR/forward.png"))
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
        self.setWindowIcon(QIcon("/home/red/toolsR/app_icon.png"))  # Ajusta la ruta del ícono según sea necesario
        self.setWindowTitle("Red Browser")
        self.resize(1024, 768)

        self.show()

    def configure_privacy_settings(self):
        """Configura ajustes de privacidad en la vista del navegador."""
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)  # Desactivar JavaScript
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)  # Desactivar plugins
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)  # Desactivar almacenamiento local
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)  # Desactivar WebGL
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)  # Desactivar carga de imágenes
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
        settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.FocusOnNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.PrintElementBackgrounds, True)
        settings.setAttribute(QWebEngineSettings.ShowScrollBars, True)
        settings.setAttribute(QWebEngineSettings.DnsPrefetchEnabled, True)
        settings.setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

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

app = QApplication([])
window = SimpleBrowser()
app.exec_()
