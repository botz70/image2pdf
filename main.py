from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import os
from PIL import Image as PILImage

from android.permissions import request_permissions, Permission

request_permissions([Permission.MANAGE_EXTERNAL_STORAGE])


class ImageToPDFApp(App):
    def build(self):
        self.title = 'Image to PDF Converter'
        # Window.size = (360, 640)  # Dimensioni tipiche di uno schermo di cellulare
        layout = BoxLayout(orientation='vertical')
        
        self.filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'], multiselect=True, path='/storage/emulated/0/')
        layout.add_widget(self.filechooser)
        
        self.filename_input = TextInput(hint_text='Enter PDF file name', size_hint=(1, 0.1), halign='center', multiline=False)
        layout.add_widget(self.filename_input)
        
        convert_button = Button(text='Convert to PDF', size_hint=(1, 0.1))
        convert_button.bind(on_press=self.convert_to_pdf)
        layout.add_widget(convert_button)
        
        return layout

    def convert_to_pdf(self, instance):
        selected_files = self.filechooser.selection
        filename = self.filename_input.text.strip()
        
        if not selected_files:
            popup = Popup(title='Error', content=Label(text='No files selected!'), size_hint=(0.5, 0.5))
            popup.open()
            return
        
        if not filename:
            popup = Popup(title='Error', content=Label(text='No file name provided!'), size_hint=(0.5, 0.5))
            popup.open()
            return
        
        images = [PILImage.open(file) for file in selected_files]
        pdf_path = os.path.join('/storage/emulated/0/', f'{filename}.pdf')
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        
        # popup = Popup(title='Success', content=Label(text=f'PDF saved to {pdf_path}'), size_hint=(0.5, 0.5))
        popup = Popup(title='Success', content=Label(text=f'PDF saved!'), size_hint=(0.5, 0.5))
        popup.open()

        # Clear the file selection and input field
        self.filechooser.selection = []
        self.filename_input.text = ''

if __name__ == '__main__':
    ImageToPDFApp().run()
