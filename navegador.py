from PyQt6.QtWidgets import*
from PyQt6.QtGui import*
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineWidgets import*
from PyQt6.QtWebEngineCore import*
import os
import sys

# Perfil de navegador en modo incógnito.
class IncognitoWebEngineProfile(QWebEngineProfile):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
        self.setPersistentStoragePath("")  # Usar un directorio vacío para almacenamiento persistente

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # PATHS
        base_dir = os.path.dirname(__file__)
        self.back_icon_path = os.path.join(base_dir, 'icons', 'back.png')
        self.forward_icon_path = os.path.join(base_dir, 'icons', 'forward.png')
        browser_icon_path = os.path.join(base_dir, 'icons', 'iconoBrowser.ico')
        self.min_icon_path = os.path.join(base_dir, 'icons', 'min2.png')
        self.max_icon_path = os.path.join(base_dir, 'icons', 'max3.png')         #los tres aun no se agregaron
        self.close_icon_path = os.path.join(base_dir, 'icons', 'close2.png')
        self.recharge_icon_path = os.path.join(base_dir, 'icons', 'recharge.png')
        homepage_path = os.path.join(base_dir, 'homepage.html')
        config_icon_path = os.path.join(base_dir, 'icons', 'config.png')
        self.visible_icon_path = os.path.join(base_dir, 'icons', 'visible.png')
        self.hidden_icon_path = os.path.join(base_dir, 'icons', 'hidden.png')
        self.url_icon_path = os.path.join(base_dir, 'icons', 'redirect.png')
        self.url_icon_path_home = os.path.join(base_dir, 'icons', 'home.png')


        # Configurar perfil del navegador en modo incógnito
        self.profile = IncognitoWebEngineProfile("IncognitoProfile")

        # Configurar vista del navegador
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl.fromLocalFile(homepage_path))

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_url_bar)

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(self.back_icon_path))
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon(self.forward_icon_path))
        self.forward_button.clicked.connect(self.browser.forward)

        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon(self.recharge_icon_path))
        self.refresh_button.clicked.connect(self.browser.reload)

        # Botón para mostrar/ocultar la barra de herramientas
        self.toggle_toolbar_button = QPushButton()
        self.toggle_toolbar_button.setIcon(QIcon(config_icon_path))
        self.toggle_toolbar_button.clicked.connect(self.toggle_tool_bar)

        # Botón de cambio de tema
        self.theme_button = QPushButton("")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Botón de refrescar página en toolbar oculta
        self.refresh_button_toolbar = QPushButton("")
        self.refresh_button_toolbar.setIcon(QIcon(self.recharge_icon_path))
        self.refresh_button_toolbar.clicked.connect(self.browser.reload)

        # Botón de redirección url IA
        self.redirect_button_toolbar = QPushButton("")
        self.redirect_button_toolbar.setIcon(QIcon(self.url_icon_path))  # Usa el ícono que prefieras
        self.redirect_button_toolbar.clicked.connect(self.redirect_to_page)

        # Botón de redirección url HOMEPAGE
        self.home_redirect_button_toolbar = QPushButton("")
        self.home_redirect_button_toolbar.setIcon(QIcon(self.url_icon_path_home))  # Usa el ícono que prefieras
        self.home_redirect_button_toolbar.clicked.connect(self.redirect_to_page_home)

        # Inicializar estado del color de tema
        self.dark_mode = False
        self.pink_mode = False 

        # Crear la barra de herramientas principal
        self.main_tool_bar = QToolBar("Main", self)
        self.main_tool_bar.setObjectName("MainToolBar")

        # Agregar el botón de cambio de tema a la barra de herramientas
        self.main_tool_bar.addWidget(self.theme_button)                 #Añadir el botones a la barra de herramientas
        self.main_tool_bar.addWidget(self.refresh_button_toolbar)
        self.main_tool_bar.addWidget(self.redirect_button_toolbar)
        self.main_tool_bar.addWidget(self.home_redirect_button_toolbar) 

        # La barra de herramientas inicia visible
        self.main_tool_bar.setVisible(True)

        # Crear barra de título personalizada
        self.create_title_bar()

        # Aplicar estilos iniciales
        self.apply_styles()

        # Configurar diseño
        self.layout = QVBoxLayout()
        self.url_layout = QHBoxLayout()
        self.url_layout.addWidget(self.back_button)
        self.url_layout.addWidget(self.forward_button)
        self.url_layout.addWidget(self.refresh_button)
        self.url_layout.addWidget(self.url_bar)
        self.url_layout.addWidget(self.toggle_toolbar_button)  # Solo agregar el botón de configuración aquí

        self.layout.addWidget(self.title_bar)  # Agregar la barra de título
        self.layout.addWidget(self.main_tool_bar)  # Agregar la barra de herramientas
        self.layout.addLayout(self.url_layout)  # La disposición de URL y el botón de configuración
        self.layout.addWidget(self.browser)

        self.main_tool_bar.setMinimumWidth(100)  # Establecer un ancho mínimo para la barra de herramientas

        # Configurar contenedor y ventana principal
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Configurar la ventana para no mostrar la barra de título nativa
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Ocultar la barra de título nativa
        self.setWindowIcon(QIcon(browser_icon_path))
        self.setWindowTitle("Red Browser")
        self.resize(1024, 768)

        # Configurar opciones de privacidad
        self.configure_privacy_settings()

        # Variables para arrastrar ventana
        self.drag_pos = None

    def redirect_to_page(self): # Define la URL a la que quieres redirigir
        new_url = "https://www.bing.com/images/create"
        self.browser.setUrl(QUrl(new_url))

    def redirect_to_page_home(self): # Define la URL a la que quieres redirigir
        new_url = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), 'homepage.html'))
        self.browser.setUrl(new_url)

    def toggle_tool_bar(self):  # Alternar visibilidad de la barra de herramientas principal
        if self.main_tool_bar.isVisible():
            self.main_tool_bar.setVisible(False)
            self.toggle_toolbar_button.setIcon(QIcon(self.hidden_icon_path))
        else:
            self.main_tool_bar.setVisible(True)
            self.toggle_toolbar_button.setIcon(QIcon(self.visible_icon_path))

    def create_title_bar(self):
        # Barra de título personalizada
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(20)
        
        # Estilo de la barra de título
        self.title_bar.setStyleSheet("")  # por defecto blanco (marco superior)

        # Botón de cerrar
        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon(self.close_icon_path))
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("border: none;")
        self.close_button.setFixedSize(40, 40)  # Ajusta el tamaño

        # Botón de minimizar
        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(QIcon(self.min_icon_path))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet("border: none;")
        self.minimize_button.setFixedSize(40, 40)  # Ajusta el tamaño

        # Botón de maximizar
        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(QIcon(self.max_icon_path))
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.maximize_button.setStyleSheet("border: none;")
        self.maximize_button.setFixedSize(40, 40)  # Ajusta el tamaño

        # Layout de la barra de título
        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(0)

        # Agrega un espaciador para alinear los botones a la derecha
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.title_layout.addItem(self.spacer)
        self.title_layout.addWidget(self.minimize_button)
        self.title_layout.addWidget(self.maximize_button)
        self.title_layout.addWidget(self.close_button)
        
        # Agregar eventos de arrastre
        self.title_bar.mousePressEvent = self.mousePressEvent
        self.title_bar.mouseMoveEvent = self.mouseMoveEvent

    # Maneja el evento de presionar el ratón para iniciar el arrastre
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    # Maneja el evento de mover el ratón para arrastrar la ventana.
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag_pos:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    # Alterna entre maximizar y restaurar la ventana
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def configure_privacy_settings(self):
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.SpatialNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PrintElementBackgrounds, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        

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
        if self.pink_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #ff61c5;
                }
                QToolBar {
                    background-color: #ffabe0;           
                }
                QWidget {
                    background-color: #ffabe0;
                    color: #78596e;
                }
                QPushButton {
                    background-color: #ffabe0;
                    color: #eee;
                    border: 1px solid #78596e;
                    padding: 5px;
                    border-radius: 5px;
                    min-width: 10px;
                    min-height: 10px;
                }
                QPushButton:hover {
                    background-color: #525252;
                }
                QPushButton:pressed {
                    background-color: #d08080;
                }
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #78596e;
                    border-radius: 5px;
                    color: #78596e;
                    background-color: #f5c5c5;
                }
                QWidget#title_bar {
                    background-color: #ffabe0;
                }
            """)
            self.theme_button.setText("Modo Oscuro")
        elif self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #131313;
                }
                QToolBar {
                    background-color: white;            
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
                    background-color: #525252;
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
                    background-color: #525252;
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
            self.theme_button.setText("Modo Pink")

    # Cambia entre modo claro y oscuro.
    def toggle_theme(self):
        if self.pink_mode:
            self.pink_mode = False
            self.dark_mode = True
        elif self.dark_mode:
            self.dark_mode = False
        else:
            self.dark_mode = False
            self.pink_mode = True

        self.apply_styles()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())