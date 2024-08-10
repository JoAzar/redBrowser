from PyQt6.QtWidgets import*
from PyQt6.QtGui import*
from PyQt6.QtCore import*
from PyQt6.QtWebEngineWidgets import*
from PyQt6.QtWebEngineCore import*
from color import*
import os
import sys
import json

# Perfil de navegador en modo incógnito.
class MainWindow2(QMainWindow):
    def __init__(self, style_sheet, main_window):
        super().__init__()

        # Guarda una referencia a la ventana principal
        self.main_window = main_window

        # Crear el widget central y el diseño
        layout = QVBoxLayout()
        central_widget = QWidget()
        self.setWindowTitle("CONFIGURACIONES")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True) #Transparente
        self.resize(300, 200)  # Ajuste del tamaño de la ventana

        # Crear y añadir los QCheckBox al diseño
        self.checkbox1 = QCheckBox("Configuration")
        self.checkbox2 = QCheckBox("Crear Imagen IA")
        self.checkbox3 = QCheckBox("Instagram")
        self.checkbox4 = QCheckBox("Otra Opcion 1")
        self.checkbox5 = QCheckBox("Otra Opcion 2")
        self.checkbox6 = QCheckBox("Otra Opcion 3")

        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.checkbox3)
        layout.addWidget(self.checkbox4)
        layout.addWidget(self.checkbox5)
        layout.addWidget(self.checkbox6)

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

        # Aplicar el estilo CSS a la ventana secundaria
        self.setStyleSheet(style_sheet)

    def show_state(self, state):
        checkbox_states = {
            "Configuration": self.checkbox1.isChecked(),
            "Crear Imagen IA": self.checkbox2.isChecked(),
            "Instagram": self.checkbox3.isChecked(),
            "Otra Opcion 1": self.checkbox4.isChecked(),
            "Otra Opcion 2": self.checkbox5.isChecked(),
            "Otra Opcion 3": self.checkbox6.isChecked()
        }
        self.main_window.update_buttons_state(checkbox_states)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar los paths desde el archivo JSON
        base_dir = os.path.dirname(__file__)
        with open(os.path.join(base_dir, 'paths.json'), 'r') as f:
            paths = json.load(f)

        self.mappage_path = os.path.join(base_dir, paths['mappage'])
        self.homepage_path = os.path.join(base_dir, paths['homepage'])
        self.back_icon_path = os.path.join(base_dir, paths['back'])
        self.back_n_icon_path = os.path.join(base_dir, paths['back_n'])
        self.forward_icon_path = os.path.join(base_dir, paths['forward'])
        self.forward_n_icon_path = os.path.join(base_dir, paths['forward_n'])
        self.browser_icon_path = os.path.join(base_dir, paths['browser'])
        self.recharge_icon_path = os.path.join(base_dir, paths['recharge'])
        self.recharge_n_icon_path = os.path.join(base_dir, paths['recharge_n'])
        self.tools_icon_path = os.path.join(base_dir, paths['tools'])
        self.tools_n_icon_path = os.path.join(base_dir, paths['tools_n'])
        self.url_icon_path = os.path.join(base_dir, paths['url'])
        self.url_n_icon_path = os.path.join(base_dir, paths['url_n'])
        self.home_icon_path = os.path.join(base_dir, paths['home'])
        self.home_n_icon_path = os.path.join(base_dir, paths['home_n'])
        self.modo_claro_icon_path = os.path.join(base_dir, paths['modo_claro'])
        self.modo_oscuro_icon_path = os.path.join(base_dir, paths['modo_oscuro'])
        self.instagram_n_icon_path = os.path.join(base_dir, paths['instagram_n'])
        self.instagram_c_icon_path = os.path.join(base_dir, paths['instagram_c'])
        self.map_n_icon_path = os.path.join(base_dir, paths['map_n'])
        self.map_c_icon_path = os.path.join(base_dir, paths['map_c'])

        # Configurar vista del navegador
        self.browser = QWebEngineView()

        self.url_bar = QLineEdit()
        self.browser.urlChanged.connect(self.update_url_bar)

        # Cargar la página de inicio
        self.load_homepage()

        #inicio la ventana del config
        self.secondary_window = None

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(self.back_n_icon_path))
        self.back_button.setToolTip("Ir hacia atrás")
        self.back_button.clicked.connect(self.browser.back)
        self.back_button.installEventFilter(self)

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon(self.forward_n_icon_path))
        self.forward_button.setToolTip("Ir hacia adelante")
        self.forward_button.clicked.connect(self.browser.forward)
        self.forward_button.installEventFilter(self)

        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon(self.recharge_n_icon_path))
        self.refresh_button.setToolTip("Refrescar")
        self.refresh_button.clicked.connect(self.browser.reload)
        self.refresh_button.installEventFilter(self)

        # Botón de redirección url HOMEPAGE
        self.home_button = QPushButton()
        self.home_button.setIcon(QIcon(self.home_n_icon_path))
        self.home_button.setToolTip("Volver al Inicio")
        self.home_button.clicked.connect(self.redirect_to_page_home)
        self.home_button.installEventFilter(self)

        #tools de navegador
        self.tools_button = QPushButton()
        self.tools_button.setIcon(QIcon(self.tools_icon_path))
        self.tools_button.setToolTip("Accesos directos")
        self.tools_button.clicked.connect(self.abrirVentanaConfig)
        self.tools_button.installEventFilter(self)

        # Botón de cambio de tema
        self.theme_button = QPushButton("")
        self.theme_button.setToolTip("Cambiar color")

        #Inicializar estado del color de tema
        self.dark_mode = False

        #Crear una instancia de ColorManager
        self.color_manager = ColorManager(
            widget=self,
            theme_button=self.theme_button,
            modo_claro_icon_path="path_to_light_mode_icon.png",
            modo_oscuro_icon_path="path_to_dark_mode_icon.png"
        )

        #Conectar el clic del botón al método toggle_theme
        self.theme_button.clicked.connect(self.color_manager.toggle_theme)
        
        # Botón de redirección url IA
        self.redirect_button_toolbar = QPushButton("")
        self.redirect_button_toolbar.setToolTip("Crear imágen con IA")
        self.redirect_button_toolbar.setIcon(QIcon(self.url_icon_path))
        self.redirect_button_toolbar.clicked.connect(self.redirect_to_page)
        self.redirect_button_toolbar.installEventFilter(self)

        # Botón de redirección url MAPS
        self.maps_redirect_button_toolbar = QPushButton("")
        self.maps_redirect_button_toolbar.setToolTip("Ver Mapas")
        self.maps_redirect_button_toolbar.setIcon(QIcon(self.map_n_icon_path))
        self.maps_redirect_button_toolbar.clicked.connect(self.redirect_to_maps)
        self.maps_redirect_button_toolbar.installEventFilter(self)

        #Botón de redirección a Instagram Color
        self.instagram_redirect_button_toolbar = QPushButton("")
        self.instagram_redirect_button_toolbar.setToolTip("Ir a Instagram")
        self.instagram_redirect_button_toolbar.setIcon(QIcon(self.instagram_c_icon_path))
        self.instagram_redirect_button_toolbar.clicked.connect(self.redirect_to_insta)
        self.instagram_redirect_button_toolbar.installEventFilter(self) #llamado a la funcion para rotar iconos || solo para iconos de barra tools
        
        # Crear la barra de herramientas principal
        self.main_tool_bar = QToolBar("Main", self)
        self.main_tool_bar.setObjectName("MainToolBar")
        self.main_tool_bar.setOrientation(Qt.Orientation.Vertical)          #orientación de la barra config en vertical

        # Agregar el botón de cambio de tema a la barra de herramientas
        self.main_tool_bar.addWidget(self.theme_button)                     #Añadir el botones a la barra de herramientas
        self.main_tool_bar.addWidget(self.redirect_button_toolbar)
        #poner otros botones del toolbar acá
        self.main_tool_bar.addWidget(self.instagram_redirect_button_toolbar)
        self.main_tool_bar.addWidget(self.maps_redirect_button_toolbar)
        
        # La barra de herramientas inicia visible
        self.main_tool_bar.setVisible(False)

        # Crear barra de título personalizada
        self.create_title_bar()

        # Aplicar estilos iniciales
        self.color_manager.apply_styles()

        # Configurar diseño
        self.main_layout = QHBoxLayout()                    # Usar un diseño horizontal para organizar la barra de herramientas y el contenido

        # Configurar el contenido principal
        self.content_layout = QVBoxLayout()                 # Diseño vertical para el contenido principal
        self.url_layout = QHBoxLayout()

        self.url_layout.addWidget(self.back_button)
        self.url_layout.addWidget(self.home_button)
        self.url_layout.addWidget(self.forward_button)
        self.url_layout.addWidget(self.refresh_button)
        self.url_layout.addWidget(self.tools_button)
        self.url_layout.addWidget(self.url_bar)

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

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            if obj == self.instagram_redirect_button_toolbar:
                self.instagram_redirect_button_toolbar.setIcon(QIcon(self.instagram_c_icon_path))
            elif obj == self.refresh_button:
                self.refresh_button.setIcon(QIcon(self.recharge_icon_path))
            elif obj == self.maps_redirect_button_toolbar:
                self.maps_redirect_button_toolbar.setIcon(QIcon(self.map_c_icon_path))
            elif obj == self.tools_button:
                self.tools_button.setIcon(QIcon(self.tools_icon_path))
            elif obj == self.forward_button:
                self.forward_button.setIcon(QIcon(self.forward_icon_path))
            elif obj == self.back_button:
                self.back_button.setIcon(QIcon(self.back_icon_path))
            elif obj == self.home_button:
                self.home_button.setIcon(QIcon(self.home_icon_path))

        elif event.type() == QEvent.Type.Leave:
            if obj == self.instagram_redirect_button_toolbar:
                self.instagram_redirect_button_toolbar.setIcon(QIcon(self.instagram_n_icon_path))
            elif obj == self.refresh_button:
                self.refresh_button.setIcon(QIcon(self.recharge_n_icon_path))
            elif obj == self.maps_redirect_button_toolbar:
                self.maps_redirect_button_toolbar.setIcon(QIcon(self.map_n_icon_path))
            elif obj == self.tools_button:
                self.tools_button.setIcon(QIcon(self.tools_n_icon_path))
            elif obj == self.forward_button:
                self.forward_button.setIcon(QIcon(self.forward_n_icon_path))
            elif obj == self.back_button:
                self.back_button.setIcon(QIcon(self.back_n_icon_path))

            elif obj == self.home_button:
                self.home_button.setIcon(QIcon(self.home_n_icon_path))
        return super().eventFilter(obj, event)

    def update_buttons_state(self, checkbox_states):
        #ACTIVAR DESACTIVAR CON CHECKBOX LA BARRA DE CONFIGURACION || Este funciona
        if(checkbox_states.get("Configuration", False) == False):
            self.main_tool_bar.setVisible(False)
        if(checkbox_states.get("Configuration", False) == True):
            self.main_tool_bar.setVisible(True)

    def abrirVentanaConfig(self):
        if self.secondary_window is None or not self.secondary_window.isVisible():
            style_sheet = self.color_manager.apply_styles()
            self.secondary_window = MainWindow2(style_sheet, self)
            initial_states = {
                "Configuration": self.secondary_window.checkbox1.isChecked(),
                "Crear Imagen IA": self.secondary_window.checkbox2.isChecked(),
                "Instagram": self.secondary_window.checkbox3.isChecked(),
                "Otra Opcion 1": self.secondary_window.checkbox4.isChecked(),
                "Otra Opcion 2": self.secondary_window.checkbox5.isChecked(),
                "Otra Opcion 3": self.secondary_window.checkbox6.isChecked()
            }  
            self.update_buttons_state(initial_states)
            main_window_pos = self.pos()
            secondary_window_pos = QPoint(main_window_pos.x() + 50, main_window_pos.y() + 100)
            self.secondary_window.move(secondary_window_pos)
            self.secondary_window.show()
        else:
            self.secondary_window.close()
            self.secondary_window = None

    def moveEvent(self, event):
        super().moveEvent(event)
        self.check_secondary_window_visibility()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.check_secondary_window_visibility()

    def check_secondary_window_visibility(self):
        if self.secondary_window and self.secondary_window.isVisible():
            self.secondary_window.close()
            self.secondary_window = None

    def load_homepage(self):
        self.browser.setUrl(QUrl.fromLocalFile(self.homepage_path))

    def redirect_to_maps(self):
        new_url = QUrl.fromLocalFile(self.mappage_path)
        self.browser.setUrl(new_url)

    def redirect_to_page(self):
        new_url = "https://www.bing.com/images/create"
        self.browser.setUrl(QUrl(new_url))

    def redirect_to_insta(self):
        new_url = "https://www.instagram.com"
        self.browser.setUrl(QUrl(new_url))

    def redirect_to_page_home(self):
        new_url = QUrl.fromLocalFile(self.homepage_path)
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

    # Actualiza la barra de direcciones con la URL actual del navegador.
    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())