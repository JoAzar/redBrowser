from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QUrl, Qt, QPoint
from PyQt5.QtGui import QIcon, QMouseEvent
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineView, QWebEngineSettings
import os
import sys

# Perfil de navegador en modo incógnito.
class IncognitoWebEngineProfile(QWebEngineProfile):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        self.setPersistentStoragePath("")  # Usar un directorio vacío para almacenamiento persistente

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Rutas de los iconos
        base_dir = os.path.dirname(__file__)
        back_icon_path = os.path.join(base_dir, 'icons', 'back.png')
        forward_icon_path = os.path.join(base_dir, 'icons', 'forward.png')
        browser_icon_path = os.path.join(base_dir, 'icons', 'iconoBrowser.ico')
        self.min_icon_path = os.path.join(base_dir, 'icons', 'min.png')
        self.max_icon_path = os.path.join(base_dir, 'icons', 'max.png')         #los tres aun no se agregaron
        self.close_icon_path = os.path.join(base_dir, 'icons', 'close.png')

        # Configurar perfil del navegador en modo incógnito
        self.profile = IncognitoWebEngineProfile("IncognitoProfile")

        # Configurar vista del navegador
        self.browser = QWebEngineView()

        # URL inicial
        ingreso = input("Ingrese su URL (sin https): ")
        self.browser.setUrl(QUrl("https://www."+ingreso+".com" ))  # Convertir la URL a QUrl

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

        # Botón de cambio de tema
        self.theme_button = QPushButton("Modo Oscuro")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Inicializar estado del tema
        self.dark_mode = False  # Asegúrate de definir el atributo `dark_mode`

        # Crear barra de título personalizada
        self.create_title_bar()

        # Aplicar estilos iniciales
        self.apply_styles()

        # Configurar diseño
        self.layout = QVBoxLayout()
        self.url_layout = QHBoxLayout()
        self.url_layout.addWidget(self.back_button)
        self.url_layout.addWidget(self.forward_button)
        self.url_layout.addWidget(self.url_bar)
        self.url_layout.addWidget(self.theme_button)    #Añadir el botón de cambio de tema
        self.layout.addWidget(self.title_bar)           #Agregar la barra de título
        self.layout.addLayout(self.url_layout)
        self.layout.addWidget(self.browser)

        # Configurar contenedor y ventana principal
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Configurar la ventana para no mostrar la barra de título nativa
        self.setWindowFlags(Qt.FramelessWindowHint)  #Ocultar la barra de título nativa
        self.setWindowIcon(QIcon(browser_icon_path))
        self.setWindowTitle("Red Browser")
        self.resize(1024, 768)

        # Configurar opciones de privacidad
        self.configure_privacy_settings()

        # Variables para arrastrar ventana
        self.drag_pos = None

    def create_title_bar(self):
        #Varra de título personalizada
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(20)
        
        # Estilo de la barra de título
        self.title_bar.setStyleSheet("")    #por defecto blanco (marco superior)

       # Botón de cerrar
        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon(self.close_icon_path))
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("border: none;")
        self.close_button.setFixedSize(30, 30)  # Ajusta el tamaño

        # Botón de minimizar
        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(QIcon(self.min_icon_path))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet("border: none;")
        self.minimize_button.setFixedSize(30, 30)  # Ajusta el tamaño

        # Botón de maximizar
        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(QIcon(self.max_icon_path))
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.maximize_button.setStyleSheet("border: none;")
        self.maximize_button.setFixedSize(30, 30)  # Ajusta el tamaño

        # Layout de la barra de título
        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(0)

        # Agrega un espaciador para alinear los botones a la derecha
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.title_layout.addItem(self.spacer)
        self.title_layout.addWidget(self.minimize_button)
        self.title_layout.addWidget(self.maximize_button)
        self.title_layout.addWidget(self.close_button)
        
        # Agregar eventos de arrastre
        self.title_bar.mousePressEvent = self.mousePressEvent
        self.title_bar.mouseMoveEvent = self.mouseMoveEvent

    #Maneja el evento de presionar el ratón para iniciar el arrastre
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    #Maneja el evento de mover el ratón para arrastrar la ventana.
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    #Alterna entre maximizar y restaurar la ventana
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def configure_privacy_settings(self):
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
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
        if not url.startswith('http'):
            url = 'https://' + url
        self.browser.setUrl(QUrl(url))

    # Actualiza la barra de direcciones con la URL actual del navegador.
    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    # Aplica estilos personalizados a los widgets.  -> #NOTA QPushButton son los botones de maxi min y cerrar
    def apply_styles(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #131313;
                    height: 50px;
                }
                QWidget {
                    background-color: #131313;
                    color: #eee;
                }
                QPushButton {
                    background-color: #131313;
                    color: #eee;
                    border: 1px solid #555;
                    padding: 5px;
                    border-radius: 5px;
                    min-width: 10px;
                    min-height: 10px;
                }
                QPushButton:hover {
                    background-color: #444;
                }
                QPushButton:pressed {
                    background-color: #555;
                }
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #555;
                    border-radius: 5px;
                    color: #eee;
                    background-color: #333;
                }
                QWidget#title_bar {
                    background-color: #131313;
                }
            """)
            self.theme_button.setText("Modo Claro")
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #000;
                }
                QWidget {
                    background-color: #fff;
                    color: #000;
                }
                QPushButton {
                    background-color: #fff;
                    color: #000;
                    border: 1px solid #ccc;
                    padding: 5px;
                    border-radius: 5px;
                    min-width: 10px;
                    min-height: 10px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
                QPushButton:pressed {
                    background-color: #e0e0e0;
                }
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    color: #000;
                    background-color: #fff;
                }
                QWidget#title_bar {
                    background-color: #fff;
                }
            """)
            self.theme_button.setText("Modo Oscuro")

    # Cambia entre modo claro y oscuro.
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_styles()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())