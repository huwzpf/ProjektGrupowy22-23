import tkinter as tk
from app.views.basic_view import BUTTON_WIDTH_1, BUTTON_HEIGHT_1, WIDTH, BUTTON_FONT, Y_MENU
from app.views.basic_choose_audio_file import BasicChooseAudioFile


class ChooseAudioForGeneratingSamplesView(BasicChooseAudioFile):

    def __init__(self, root, voice_model_service, voice_records_service):
        super(ChooseAudioForGeneratingSamplesView, self).__init__(root, voice_model_service, voice_records_service)
        main_menu_button = tk.Button(self.root, text="Main menu", command=self.switch_to_main_view,
                                     width=BUTTON_WIDTH_1, height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        continue_button = tk.Button(self.root, text="Generate samples", command=self.open_file, width=BUTTON_WIDTH_1,
                                    height=BUTTON_HEIGHT_1, font=BUTTON_FONT)
        main_menu_button.place(x=WIDTH / 2 - 520, y=Y_MENU)
        continue_button.place(x=WIDTH / 2 + 120, y=Y_MENU)
