from PyQt6.QtWidgets import*
from PyQt6.QtGui import*
from PyQt6.QtCore import*
from PyQt6.QtWebEngineWidgets import*
from PyQt6.QtWebEngineCore import*
import os
import sys


# Perfil de navegador en modo incógnito.
class IncognitoWebEngineProfile(QWebEngineProfile):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
        self.setPersistentStoragePath("")

class MainWindow2(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear el widget central y el diseño
        layout = QVBoxLayout()
        central_widget = QWidget()
        self.setWindowTitle("CONFIGURACIONES")
        self.resize(300, 100)
        # Crear el QCheckBox
        self.checkbox1 = QCheckBox()
        self.checkbox1.setText("Cambiar Color")
        self.checkbox1.setCheckState(Qt.CheckState.Unchecked)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Quitar el marco y la barra de título
        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Hacer que el fondo sea transparente

        # Crear el QCheckBox
        self.checkbox2 = QCheckBox()
        self.checkbox2.setText("Crear Imagen IA")
        self.checkbox2.setCheckState(Qt.CheckState.Unchecked)

        # Crear el QCheckBox
        self.checkbox3 = QCheckBox()
        self.checkbox3.setText("Instagram")
        self.checkbox3.setCheckState(Qt.CheckState.Unchecked)

        # Crear el QCheckBox
        self.checkbox4 = QCheckBox()
        self.checkbox4.setText("Otra Opcion 1")
        self.checkbox4.setCheckState(Qt.CheckState.Unchecked)

        # Crear el QCheckBox
        self.checkbox5 = QCheckBox()
        self.checkbox5.setText("Otra Opcion 2")
        self.checkbox5.setCheckState(Qt.CheckState.Unchecked)

        # Crear el QCheckBox
        self.checkbox6 = QCheckBox()
        self.checkbox6.setText("Otra Opcion 3")
        self.checkbox6.setCheckState(Qt.CheckState.Unchecked)
        
        # Añadir el QCheckBox al diseño
        layout.addWidget(self.checkbox1, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.checkbox2, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.checkbox3, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.checkbox4, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.checkbox5, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.checkbox6, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        # Establecer el diseño en el widget central
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Conectar la señal stateChanged a show_state
        self.checkbox1.stateChanged.connect(self.show_state)
        self.checkbox2.stateChanged.connect(self.show_state)
        self.checkbox3.stateChanged.connect(self.show_state)
        self.checkbox4.stateChanged.connect(self.show_state)
        self.checkbox5.stateChanged.connect(self.show_state)
        self.checkbox6.stateChanged.connect(self.show_state)

        # Aplicar un estilo CSS para bordes redondeados
        self.setStyleSheet("""
            QMainWindow {
                border-radius: 15px;
                border: 2px solid #000;  /* Color y grosor del borde */
                padding: 5px;
            }
        """)

    #FUNCIONES DE MAIN 2    
    def show_state(self, state):
        for checkbox in [self.checkbox1, self.checkbox2, self.checkbox3, self.checkbox4, self.checkbox5, self.checkbox6]:
            if checkbox.checkState() == Qt.CheckState.Checked:
                print(f"{checkbox.text()}: Marcado")
            else:
                print(f"{checkbox.text()}: No marcado")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # PATHS
        base_dir = os.path.dirname(__file__)
        self.back_icon_path = os.path.join(base_dir, 'icons', 'back.png')
        self.back_n_icon_path = os.path.join(base_dir, 'icons', 'back_n.png')

        self.forward_icon_path = os.path.join(base_dir, 'icons', 'forward.png')
        self.forward_n_icon_path = os.path.join(base_dir, 'icons', 'forward_n.png')

        self.browser_icon_path = os.path.join(base_dir, 'icons', 'iconoBrowser.ico')

        self.recharge_icon_path = os.path.join(base_dir, 'icons', 'recharge.png')
        self.recharge_n_icon_path = os.path.join(base_dir, 'icons', 'recharge_n.png')

        homepage_path = os.path.join(base_dir, 'public/homepage.html')

        config_icon_path = os.path.join(base_dir, 'icons', 'config.png')
        config_n_icon_path = os.path.join(base_dir, 'icons', 'config_n.png')

        self.visible_icon_path = os.path.join(base_dir, 'icons', 'visible.png')
        self.visible_n_icon_path = os.path.join(base_dir, 'icons', 'visible_n.png')

        self.hidden_icon_path = os.path.join(base_dir, 'icons', 'hidden.png')
        self.hidden_n_icon_path = os.path.join(base_dir, 'icons', 'hidden_n.png')

        self.url_icon_path = os.path.join(base_dir, 'icons', 'redirect.png')
        self.url_n_icon_path = os.path.join(base_dir, 'icons', 'redirect_n.png')

        self.url_icon_path_home = os.path.join(base_dir, 'icons', 'home.png')
        self.url_n_icon_path_home = os.path.join(base_dir, 'icons', 'home_n.png')

        self.modo_claro_icon_path = os.path.join(base_dir, 'icons', 'claro.png')
        self.modo_oscuro_icon_path = os.path.join(base_dir, 'icons', 'oscuro.png')
        self.modo_pink_icon_path = os.path.join(base_dir, 'icons', 'pink.png')

        self.instagram_n_icon_path = os.path.join(base_dir, 'icons', 'instagram_n.png')
        self.instagram_c_icon_path = os.path.join(base_dir, 'icons', 'instagram_c.png')

        self.map_n_icon_path = os.path.join(base_dir, 'icons', 'map_n.png')     #FALTAN LOS BOTONES
        self.map_c_icon_path = os.path.join(base_dir, 'icons', 'map_c.png')

        self.config_icon_path = os.path.join(base_dir, 'icons', 'configuracion.png')
        

        # Configurar perfil del navegador en modo incógnito
        self.profile = IncognitoWebEngineProfile("IncognitoProfile")

        # Configurar vista del navegador
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl.fromLocalFile(homepage_path))

        self.url_bar = QLineEdit()
        #self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_url_bar)

        #inicio la ventana del config
        self.secondary_window = None

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(self.back_icon_path))
        self.back_button.setToolTip("Ir hacia atrás")
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon(self.forward_icon_path))
        self.forward_button.setToolTip("Ir hacia adelante")
        self.forward_button.clicked.connect(self.browser.forward)

        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon(self.recharge_icon_path))
        self.refresh_button.setToolTip("Refrescar")
        self.refresh_button.clicked.connect(self.browser.reload)

        self.config_button = QPushButton()
        self.config_button.setIcon(QIcon(self.config_icon_path))
        self.config_button.setToolTip("Configuración")
        self.config_button.clicked.connect(self.abrirVentanaConfig)

        # Botón para mostrar/ocultar la barra de herramientas
        self.toggle_toolbar_button = QPushButton()
        self.toggle_toolbar_button.setIcon(QIcon(config_icon_path))
        self.toggle_toolbar_button.setToolTip("Herramientas")
        self.toggle_toolbar_button.clicked.connect(self.toggle_tool_bar)

        # Botón de cambio de tema
        self.theme_button = QPushButton("")
        self.theme_button.setToolTip("Cambiar color")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Botón de refrescar página en toolbar oculta
        self.refresh_button_toolbar = QPushButton("")
        self.refresh_button_toolbar.setToolTip("Refrescar")
        self.refresh_button_toolbar.setIcon(QIcon(self.recharge_n_icon_path))
        self.refresh_button_toolbar.clicked.connect(self.browser.reload)

        #llamado a la funcion para rotar iconos
        self.refresh_button_toolbar.installEventFilter(self)

        # Botón de redirección url IA
        self.redirect_button_toolbar = QPushButton("")
        self.redirect_button_toolbar.setToolTip("Crear imágen con IA")
        self.redirect_button_toolbar.setIcon(QIcon(self.url_icon_path))
        self.redirect_button_toolbar.clicked.connect(self.redirect_to_page)

        # Botón de redirección url MAPS
        self.maps_redirect_button_toolbar = QPushButton("")
        self.maps_redirect_button_toolbar.setToolTip("Ver Mapas")
        self.maps_redirect_button_toolbar.setIcon(QIcon(self.map_n_icon_path))
        self.maps_redirect_button_toolbar.clicked.connect(self.redirect_to_maps)

        # Botón de redirección url HOMEPAGE
        self.home_redirect_button_toolbar = QPushButton("")
        self.home_redirect_button_toolbar.setToolTip("Volver al Inicio")
        self.home_redirect_button_toolbar.setIcon(QIcon(self.url_icon_path_home))
        self.home_redirect_button_toolbar.clicked.connect(self.redirect_to_page_home)

        #Botón de redirección a Instagram Color
        self.instagram_redirect_button_toolbar = QPushButton("")
        self.instagram_redirect_button_toolbar.setToolTip("Ir a Instagram")
        self.instagram_redirect_button_toolbar.setIcon(QIcon(self.instagram_c_icon_path))
        self.instagram_redirect_button_toolbar.clicked.connect(self.redirect_to_insta)

        #llamado a la funcion para rotar iconos
        self.instagram_redirect_button_toolbar.installEventFilter(self)

        # Inicializar estado del color de tema
        self.dark_mode = False
        self.pink_mode = False 

        # Crear la barra de herramientas principal
        self.main_tool_bar = QToolBar("Main", self)
        self.main_tool_bar.setObjectName("MainToolBar")
        self.main_tool_bar.setOrientation(Qt.Orientation.Vertical)          #orientación de la barra config en vertical

        # Agregar el botón de cambio de tema a la barra de herramientas
        self.main_tool_bar.addWidget(self.theme_button)                     #Añadir el botones a la barra de herramientas
        self.main_tool_bar.addWidget(self.refresh_button_toolbar)
        self.main_tool_bar.addWidget(self.redirect_button_toolbar)
        self.main_tool_bar.addWidget(self.home_redirect_button_toolbar)
        self.main_tool_bar.addWidget(self.instagram_redirect_button_toolbar)
        self.main_tool_bar.addWidget(self.maps_redirect_button_toolbar)
        
        # La barra de herramientas inicia visible
        self.main_tool_bar.setVisible(True)

        # Crear barra de título personalizada
        self.create_title_bar()

        # Aplicar estilos iniciales
        self.apply_styles()

        # Configurar diseño
        self.main_layout = QHBoxLayout()                    # Usar un diseño horizontal para organizar la barra de herramientas y el contenido

        # Configurar el contenido principal
        self.content_layout = QVBoxLayout()                 # Diseño vertical para el contenido principal
        self.url_layout = QHBoxLayout()

        self.url_layout.addWidget(self.back_button)
        self.url_layout.addWidget(self.forward_button)
        self.url_layout.addWidget(self.refresh_button)
        self.url_layout.addWidget(self.config_button)
        self.url_layout.addWidget(self.url_bar)
        self.url_layout.addWidget(self.toggle_toolbar_button)

        self.content_layout.addWidget(self.title_bar)       # Agregar la barra de título
        self.content_layout.addLayout(self.url_layout)      # La disposición de URL y el botón de configuración
        self.content_layout.addWidget(self.browser)         # Agregar el navegador

        # Agregar la barra de herramientas vertical a la derecha
        self.config_bar = QVBoxLayout()
        self.config_bar.addWidget(self.main_tool_bar)

        # Añadir el contenido principal y la barra de herramientas al diseño principal
        self.main_layout.addLayout(self.content_layout) 
        self.main_layout.addLayout(self.config_bar)  

        # Configurar contenedor y ventana principal
        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)

        app.setStyle("Fusion")
        self.setWindowIcon(QIcon(self.browser_icon_path))
        self.setWindowTitle("Red Browser")

        largo = 1024
        ancho = 860
        self.resize(largo, ancho)

        # Configurar opciones de privacidad
        self.configure_privacy_settings()


    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            if obj == self.instagram_redirect_button_toolbar:
                self.instagram_redirect_button_toolbar.setIcon(QIcon(self.instagram_c_icon_path))
            elif obj == self.refresh_button_toolbar:
                self.refresh_button_toolbar.setIcon(QIcon(self.recharge_icon_path))
            elif obj == self.maps_redirect_button_toolbar:
                self.maps_redirect_button_toolbar.setIcon(QIcon(self.map_c_icon_path))

        elif event.type() == QEvent.Type.Leave:
            if obj == self.instagram_redirect_button_toolbar:
                self.instagram_redirect_button_toolbar.setIcon(QIcon(self.instagram_n_icon_path))
            elif obj == self.refresh_button_toolbar:
                self.refresh_button_toolbar.setIcon(QIcon(self.recharge_n_icon_path))
            elif obj == self.maps_redirect_button_toolbar:
                self.maps_redirect_button_toolbar.setIcon(QIcon(self.map_n_icon_path))
        return super().eventFilter(obj, event)


    def abrirVentanaConfig(self):
        if self.secondary_window is None or not self.secondary_window.isVisible():
            self.secondary_window = MainWindow2()
            self.secondary_window.show()
        else:
            self.secondary_window.close()
            self.secondary_window = None

    def redirect_to_maps(self):
        new_url = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), 'public/map.html'))
        self.browser.setUrl(new_url)

    def redirect_to_page(self):
        new_url = "https://www.bing.com/images/create"
        self.browser.setUrl(QUrl(new_url))

    def redirect_to_insta(self):
        new_url = "https://www.instagram.com"
        self.browser.setUrl(QUrl(new_url))

    def redirect_to_page_home(self):
        new_url = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), 'public/homepage.html'))
        self.browser.setUrl(new_url)

    def toggle_tool_bar(self):  # Alternar visibilidad de la barra de herramientas principal
        if self.main_tool_bar.isVisible():
            self.main_tool_bar.setVisible(False)
            self.toggle_toolbar_button.setIcon(QIcon(self.hidden_icon_path))
        else:
            self.main_tool_bar.setVisible(True)
            self.toggle_toolbar_button.setIcon(QIcon(self.visible_icon_path))

    def create_title_bar(self):
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(0) #altura del margen superior
        self.title_bar.setStyleSheet("")

        # Layout de la barra de título
        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(0)

        # Agrega un espaciador para alinear los botones a la derecha
        self.spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.title_layout.addItem(self.spacer)

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
                QToolTip {
                    background-color: white;
                    color: black;
                    border: 1px solid black;
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
                    background-color: #ffcfcf;
                }
                QPushButton:pressed {
                    background-color: #ffcfcf;
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
            self.theme_button.setIcon(QIcon(self.modo_oscuro_icon_path))
        elif self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #131313;
                }
                QToolTip {
                    background-color: white;
                    color: #eee;
                    border: 1px solid black;
                    padding: 5px;
                    border-radius: 30px;
                }
                QToolTip {
                    background-color: white;
                    color: black;
                    border: 1px solid black;
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
                    background-color:   #ffffff;
                    color: black;
                }
                QPushButton:pressed {
                    background-color:   #ffffff;
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
            self.theme_button.setIcon(QIcon(self.modo_claro_icon_path))
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #000;
                }
                QToolTip {
                    background-color: white;
                    color: black;
                    border: 1px solid black;
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
                    background-color:  #686868;
                    color:  #ffffff;
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
            self.theme_button.setIcon(QIcon(self.modo_pink_icon_path))

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