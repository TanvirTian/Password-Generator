import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget, QTabWidget, QMessageBox,QComboBox,QMenuBar,QAction,QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
import qrcode
import string
import random
import pyperclip
import threading




class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()     
        #main window starts here
        self.setWindowTitle("Password Generator")
        self.setFixedSize(600, 400)
        icon = QIcon("icons/icon.ico")  
        self.setWindowIcon(icon)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)        

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)  
   

        #file menu goes here
        self.menu_bar = self.menuBar()  
        self.file_menu = self.menu_bar.addMenu("File")  

        #preference menu
        self.preference_menu = self.file_menu.addMenu("Preference")
   
        #theme sub menu
        self.theme_submenu = QMenu("Themes", self)
        self.preference_menu.addMenu(self.theme_submenu)

                                 

        def make_lambda(theme):
            return lambda _: self.apply_theme(theme)

        
        themes = ["Default", "Ubuntu", "Aqua", "MacOS", "Neon", "MaterialDark", "AMOLED", "ConsoleStyle", "ElegantDark","ManjaroMix"]
        for theme in themes:
            theme_action = QAction(theme, self)
            theme_action.triggered.connect(make_lambda(theme))
            self.theme_submenu.addAction(theme_action)
            self.default_stylesheet = None
            self.load_default_theme()     
  

        #quit option
        self.quit_action = QAction("Quit", self)  
        self.quit_action.triggered.connect(self.close)  
        self.file_menu.addAction(self.quit_action) 
        #file menu ends here 

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.password_tab = QWidget()
        self.icon_label = QLabel(self)
        self.icon_label.setGeometry(600,600,10,10)
        self.history_tab = QWidget()
        
        self.tab_widget.addTab(self.password_tab, QIcon("icons/home.png"), "Generator")
        self.tab_widget.addTab(self.history_tab, QIcon("icons/list.png"),"History")
        

        self.init_password_tab()
        self.init_history_tab()
       


    def load_default_theme(self):
        self.default_stylesheet = self.styleSheet() 


    def apply_theme(self, selected_theme):
        theme_stylesheets = {
            "Ubuntu": "styles/Ubuntu.qss",
            "Aqua": "styles/aqua.qss",
            "MacOS": "styles/MacOS.qss",
            "Neon": "styles/NeonButtons.qss",
            "MaterialDark": "styles/MaterialDark.qss",
            "AMOLED": "styles/AMOLED.qss",
            "ConsoleStyle": "styles/ConsoleStyle.qss",
            "ElegantDark": "styles/ElegantDark.qss",
            "ManjaroMix": "styles/ManjaroMix.qss"
        }

        if selected_theme in theme_stylesheets:
            stylesheet_path = theme_stylesheets[selected_theme]
            with open(stylesheet_path, 'r') as file:
                self.setStyleSheet(file.read())
        elif selected_theme == "Default":
            self.setStyleSheet(self.default_stylesheet)  

         

    def init_password_tab(self):
        generate_icon = QIcon('icons/generate.png')
        qr_icon = QIcon('icons/qr.png')
        clipboard_icon = QIcon("icons/clipboard.png")
        
        self.password_tab.layout = QVBoxLayout()

        
        self.label = QLabel(self)
        pixmap = QPixmap("icons/banner.png")  
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.entry1 = QLineEdit()
        self.entry1.setPlaceholderText("Generated Password")
        self.entry1.setDisabled(True)



        self.entry2 = QLineEdit()
        self.entry2.setPlaceholderText("Password Length")

        self.button1 = QPushButton("Generate",self)
        self.button1.setFixedSize(100, 30) 
        self.button1.clicked.connect(self.generate)
        self.button1.setIcon(generate_icon)

        
        self.button_copy = QPushButton("Copy to Clipboard")
        self.button_copy.setEnabled(False)
        self.button_copy.setFixedSize(150, 30) 
        self.button_copy.clicked.connect(self.copy_to_clipboard)
        self.button_copy.setIcon(clipboard_icon)
        



        self.qrcode_button = QPushButton("Generate QR CODE")
        self.qrcode_button.setFixedSize(160, 30)
        self.qrcode_button.setIcon(qr_icon) 

        self.qrcode_button.setEnabled(False)
        self.qrcode_button.clicked.connect(self.generate_qr_code_thread)

        self.label1 = QLabel("Password Length is: 0", alignment=Qt.AlignCenter)
        self.label_strength = QLabel("Strength: Very Weak", alignment=Qt.AlignCenter)


        self.password_tab.layout.addWidget(self.label)
        self.password_tab.layout.addWidget(self.entry1)
        self.password_tab.layout.addWidget(self.entry2)
        self.password_tab.layout.addWidget(self.button1)
        self.password_tab.layout.addWidget(self.button_copy)
        self.password_tab.layout.addWidget(self.qrcode_button)
        self.password_tab.layout.addWidget(self.label1)
        self.password_tab.layout.addWidget(self.label_strength)

        self.password_tab.setLayout(self.password_tab.layout)

    

    
    def init_history_tab(self):
        clear_icon = QIcon('icons/trash.png')
        self.history_tab.layout = QVBoxLayout()

        self.history_label = QLabel("Password History:", alignment=Qt.AlignCenter)
        self.history_listbox = QListWidget()
        self.history_listbox.itemDoubleClicked.connect(self.show_selected_password)

        self.clear_history_button = QPushButton(self)
        self.clear_history_button.setFixedSize(30,40) 
        self.clear_history_button.clicked.connect(self.clear_history)
        self.clear_history_button.setIcon(clear_icon)

        scrollbar_layout = QHBoxLayout()
        scrollbar_layout.addWidget(self.history_listbox)
        scrollbar_layout.addWidget(self.history_listbox.verticalScrollBar())

        self.history_tab.layout.addWidget(self.history_label)
        self.history_tab.layout.addLayout(scrollbar_layout)
        self.history_tab.layout.addWidget(self.clear_history_button)

        self.history_tab.setLayout(self.history_tab.layout)
    
     

    def generate(self):
        get_text = self.entry2.text()
        if get_text.isdigit():  
            get = int(get_text)
        else:
            QMessageBox.information(self, "Invalid Input", "Please enter a valid integer for password length.")
            get = 8 

        words = string.ascii_letters
        symbols = string.punctuation
        nums = string.digits

        combination = words + symbols + nums
        password = ''.join(random.choice(combination) for i in range(get))

        if len(password) < 8:
            QMessageBox.information(self, "WARNING", "PASSWORD CAN'T BE LESS THAN 8 CHARACTERS!")
        else:
            self.entry1.setEnabled(True)
            self.entry1.setText(password)
            self.entry1.setDisabled(True)
            self.random_colors()
            x = len(password)
            self.label1.setText(f"Password Length is: {x}")
            self.strength_indicator(password)
            self.button_copy.setEnabled(True)
            self.qrcode_button.setEnabled(True)
            self.save_to_history(password)

    def random_colors(self):
        colors = ["red", "blue", "green", "pink", "yellow", "lightblue", "grey", "lightgreen", "orange", "gold"]
        randomc = random.choice(colors)
        self.label.setStyleSheet(f"background-color: {randomc};")

    
    
    def strength_indicator(self,password):
        length_factor = min(len(password) // 4, 4)
        
        strength_text = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"][min(length_factor, 4)]
        strength_color = ["red", "orange", "yellow", "green", "darkgreen"][min(length_factor, 4)]

        self.label_strength.setText(f"Strength: {strength_text}")
        self.label_strength.setStyleSheet(f"color: {strength_color};")
              
    
    def save_to_history(self, password):
        self.history_listbox.addItem(password)

    def show_selected_password(self):
        selected_items = self.history_listbox.selectedItems()
        if selected_items:
            selected_password = selected_items[0].text()
            QMessageBox.information(self, "Selected Password", f"The selected password is: {selected_password}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a password to view.")

    def clear_history(self):
        if self.history_listbox.count() == 0:
            QMessageBox.information(self, "History Is Empty", "Password history is Empty")    
        else:
            self.history_listbox.clear()
            QMessageBox.information(self, "History Cleared", "Password history has been cleared.")    

    def copy_to_clipboard(self):
        password = self.entry1.text()
        pyperclip.copy(password)
        QMessageBox.information(self, "Copied", "Password copied to clipboard!")

    def generate_qr_code_thread(self):
        password = self.entry1.text()
        qr_thread = threading.Thread(target=self.generate_qr_code, args=(password,))
        qr_thread.start()

    def generate_qr_code(self, password):
        if password:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4)
            qr.add_data(password)
            qr.make(fit=True)

            

            img = qr.make_image(fill_color="black", back_color="white")
            img.show()
        else:
            QMessageBox.information(self, "Warning", "Please generate a password first.")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()  
    sys.exit(app.exec_())    
