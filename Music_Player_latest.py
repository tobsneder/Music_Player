import configparser
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from mutagen.mp3 import MP3
import qdarktheme

INI_FILE_PATH = 'src/songs_config.ini'
INI_FILE_VAR_NAMES = ['song_name', 'song_artist', 'song_genre', 'song_png', 'song_mp3']


def seconds_to_timestamp(tsecs: int):
    hours = int(tsecs / 3600)
    mins = int((tsecs / 60) % 60)
    secs = tsecs % 60
    if hours == 0:
        if secs < 10:
            return f"{mins}:0{secs}"
        else:
            return f"{mins}:{secs}"
    else:
        if secs < 10 and mins < 10:
            return f"{hours}:0{mins}:0{secs}"
        elif secs < 10 and mins >= 10:
            return f"{hours}:{mins}:0{secs}"
        elif secs >= 10 and mins < 10:
            return f"{hours}:0{mins}:{secs}"
        elif secs >= 10 and mins >= 10:
            return f"{hours}:{mins}:{secs}"


class Song:
    def __init__(self, title: str, interpret: str, genre: str, pic_path: str, media_path: str):
        self.title = title
        self.interpret = interpret
        self.genre = genre
        self.pic_path = pic_path
        self.media_path = media_path

    def get_title(self):
        return self.title

    def get_interpret(self):
        return self.interpret

    def get_genre(self):
        return self.genre

    def get_duration(self):
        audio = MP3(self.media_path)
        return int(audio.info.length)

    def get_pic_path(self):
        return self.pic_path

    def get_media_path(self):
        return self.media_path

    def add_song_to_file(self,):
        pass

    @staticmethod
    def load_songs_from_file_as_objects():
        song_objects_list = []
        tmp_song_attributes = []
        ini_config_parser = configparser.ConfigParser()
        ini_config_parser.read(INI_FILE_PATH)

        for section in ini_config_parser.sections():
            for var in INI_FILE_VAR_NAMES:
                tmp_song_attributes.append(ini_config_parser.get(section, var))
            song_objects_list.append(Song(tmp_song_attributes[0], tmp_song_attributes[1], tmp_song_attributes[2],
                                          tmp_song_attributes[3], tmp_song_attributes[4]))
            tmp_song_attributes.clear()

        return song_objects_list


class PopUpWindow(QMainWindow):
    def __init__(self):
        super(PopUpWindow, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle("Anmeldung Spotify 2.0 - 4cHEL")
        self.setWindowIcon(QIcon("src/icon.png"))

        self.widget_main = QWidget()
        self.setCentralWidget(self.widget_main)
        self.layout_main = QVBoxLayout(self.widget_main)

        self.build_gui()
        self.show()

    def build_gui(self):
        self.label_header = QLabel("Spotify 2.0")
        self.lineedit_user = QLineEdit()
        self.lineedit_user.setPlaceholderText("Username")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setPlaceholderText("Password")
        self.lineedit_password.setEchoMode(0)
        self.button_submit = QPushButton("Login")
        self.button_submit.clicked.connect(self.login_pressed)

        self.layout_main.addWidget(self.label_header)
        self.layout_main.addWidget(self.lineedit_user)
        self.layout_main.addWidget(self.lineedit_password)
        self.layout_main.addWidget(self.button_submit)

    def login_pressed(self):
        username = self.lineedit_user.text()
        password = self.lineedit_password.text()
        print(username, password)
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 950, 400)
        self.setMinimumSize(950, 400)

        self.setWindowTitle("Music Player 4cHEL")
        self.setWindowIcon(QIcon("src/icon.png"))

        self.current_song = None

        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.update_song_progress)

        self.build_gui()
        self.fetch_songs()

        # show main window
        self.show()

    def fetch_songs(self):
        for i in range(len(songs)):
            self.playlist_table.setItem(i, 0, QTableWidgetItem(songs[i].get_title()))
            self.playlist_table.setItem(i, 1, QTableWidgetItem(songs[i].get_interpret()))
            self.playlist_table.setItem(i, 2, QTableWidgetItem(songs[i].get_genre()))
            self.playlist_table.setItem(i, 3, QTableWidgetItem(str(seconds_to_timestamp(songs[i].get_duration()))))

    def load_song(self):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.current_song.get_media_path())))
        self.current_song_label.setText(self.current_song.get_title())
        self.song_image_viewer.setPixmap(QPixmap.fromImage(QImage(self.current_song.get_pic_path())))

    def song_selected(self, row):
        self.song_play_button.setText("Play")
        self.current_song = songs[row]
        self.load_song()

    def song_instantplay(self, row):
        self.current_song = songs[row]
        self.load_song()
        self.music_play_pause()

    def update_song_progress(self, position):
        if self.player.state() != 0:
            song_progress_percentage = int(((position/1000)/self.current_song.get_duration())*100)
            self.song_progress.setValue(song_progress_percentage)
            self.song_progress.update()
            self.song_progress_time_label.setText(seconds_to_timestamp(int(position/1000)))
        else:
            self.song_progress.setValue(0)
            self.song_progress.update()
            self.song_progress_time_label.setText("")

    def music_shuffle(self):
        pass

    def music_back(self):
        if self.playlist_table.currentRow() > 0 :
            self.playlist_table.selectRow(songs.index(self.current_song) - 1)
            self.song_selected(songs.index(self.current_song) - 1)
            self.load_song()
            self.music_play_pause()

    def music_play_pause(self):
        if self.current_song is not None:
            if self.player.state() == 2 or self.player.state() == 0:
                self.player.play()
                self.song_play_button.setText("Pause")
            elif self.player.state() == 1:
                self.player.pause()
                self.song_play_button.setText("Play")

    def music_next(self):
        if self.playlist_table.currentRow() < len(songs) - 1:
            self.playlist_table.selectRow(songs.index(self.current_song) + 1)
            self.song_selected(songs.index(self.current_song) + 1)
            self.load_song()
            self.music_play_pause()

    def music_settings(self):
        self.popup = PopUpWindow()

    def EQ_bass_mode_selected(self):
        mode_selected = self.sender()
        if mode_selected.modename == "Bass Booster":
            self.EQ_low_slider.setValue(15)
            self.EQ_mid_slider.setValue(7)

        if mode_selected.modename == "Normal":
            self.EQ_low_slider.setValue(0)
            self.EQ_mid_slider.setValue(0)

    def EQ_modes_selection_changed(self):
        mode_selected = self.sender()

        if mode_selected.currentText() == "Jazz":
            self.EQ_low_slider.setValue(-1)
            self.EQ_mid_slider.setValue(5)
            self.EQ_high_slider.setValue(3)

        if mode_selected.currentText() == "Rock":
            self.EQ_low_slider.setValue(7)
            self.EQ_mid_slider.setValue(5)
            self.EQ_high_slider.setValue(-3)

        if mode_selected.currentText() == "Pop":
            self.EQ_low_slider.setValue(5)
            self.EQ_mid_slider.setValue(10)
            self.EQ_high_slider.setValue(10)

        if mode_selected.currentText() == "Movie":
            self.EQ_low_slider.setValue(5)
            self.EQ_mid_slider.setValue(-5)
            self.EQ_high_slider.setValue(10)

        if mode_selected.currentText() == "Custom":
            self.EQ_low_slider.setEnabled(True)
            self.EQ_mid_slider.setEnabled(True)
            self.EQ_high_slider.setEnabled(True)
            self.EQ_mode_bass_boosted.setEnabled(True)
            self.EQ_mode_normal.setEnabled(True)

        else:
            self.EQ_low_slider.setEnabled(False)
            self.EQ_mid_slider.setEnabled(False)
            self.EQ_high_slider.setEnabled(False)
            self.EQ_mode_bass_boosted.setEnabled(False)
            self.EQ_mode_normal.setEnabled(False)

    def EQ_enable_checkbox_toggled(self):
        if self.EQ_enable_checkbox.isChecked():
            self.EQ_label.setText("Equalizer enabled")
            self.EQ_select.setEnabled(True)
            self.EQ_low_slider.setEnabled(True)
            self.EQ_mid_slider.setEnabled(True)
            self.EQ_high_slider.setEnabled(True)
            self.EQ_mode_bass_boosted.setEnabled(True)
            self.EQ_mode_normal.setEnabled(True)
        else:
            self.EQ_label.setText("Equalizer disabled")
            self.EQ_select.setEnabled(False)
            self.EQ_low_slider.setEnabled(False)
            self.EQ_mid_slider.setEnabled(False)
            self.EQ_high_slider.setEnabled(False)
            self.EQ_mode_bass_boosted.setEnabled(False)
            self.EQ_mode_normal.setEnabled(False)

    def theme_checkbox_toggled(self):
        if self.theme_checkbox.isChecked():
            self.setStyleSheet(qdarktheme.load_stylesheet("dark"))
        else:
            self.setStyleSheet(qdarktheme.load_stylesheet("light"))

    def window_on_top_checkbox_toggled(self):
        if self.window_on_top_checkbox.isChecked():
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    # noinspection PyArgumentList
    def build_gui(self):
        #### main layout ####
        self.widget_main = QWidget()
        self.setCentralWidget(self.widget_main)
        self.layout_main = QGridLayout(self.widget_main)

        # info
        self.info_label = QLabel("Songs")
        self.layout_main.addWidget(self.info_label, 0, 0)

        # song select
        self.playlist_table = QTableWidget()
        self.playlist_table.setRowCount(len(songs))
        self.playlist_table.setColumnCount(4)
        self.playlist_table.setHorizontalHeaderLabels(["Title", "Interpret", "Genre", "Duration"])
        self.playlist_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.playlist_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.playlist_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.playlist_table.verticalHeader().setVisible(False)

        self.playlist_table.cellClicked.connect(self.song_selected)
        self.playlist_table.cellDoubleClicked.connect(self.song_instantplay)

        self.layout_main.addWidget(self.playlist_table, 1, 0, 3, 1)

        # current song
        self.current_song_label = QLabel("Current Song")
        self.layout_main.addWidget(self.current_song_label, 0, 1, 1, 5, alignment=Qt.AlignCenter)

        # song image
        self.song_image_viewer = QLabel()
        self.song_image_viewer.setScaledContents(True)
        self.song_image_viewer.setFixedSize(300, 300)
        self.movie = QMovie("src/cat.gif")
        self.song_image_viewer.setMovie(self.movie)
        self.movie.start()
        self.layout_main.addWidget(self.song_image_viewer, 1, 1, 1, 5, alignment=Qt.AlignCenter)

        # progress bar
        self.song_progress = QProgressBar()
        self.song_progress.setTextVisible(False)

        self.song_progress_time_label = QLabel()

        self.layout_main.addWidget(self.song_progress, 2, 1, 1, 5)
        self.layout_main.addWidget(self.song_progress_time_label, 2, 1, 1, 5, alignment=Qt.AlignCenter)

        # buttons
        self.shuffle_button = QPushButton("Shuffle")
        self.song_back_button = QPushButton("Back")
        self.song_play_button = QPushButton("Play")
        self.song_next_button = QPushButton("Next")
        self.settings_button = QPushButton("Settings")

        self.shuffle_button.clicked.connect(self.music_shuffle)
        self.song_back_button.clicked.connect(self.music_back)
        self.song_play_button.clicked.connect(self.music_play_pause)
        self.song_next_button.clicked.connect(self.music_next)
        self.settings_button.clicked.connect(self.music_settings)

        self.layout_main.addWidget(self.shuffle_button, 3, 1)
        self.layout_main.addWidget(self.song_back_button, 3, 2)
        self.layout_main.addWidget(self.song_play_button, 3, 3)
        self.layout_main.addWidget(self.song_next_button, 3, 4)
        self.layout_main.addWidget(self.settings_button, 3, 5)

        # EQ
        self.group_EQ = QGroupBox("Equalizer")
        self.layout_EQ = QGridLayout(self.group_EQ)

        self.EQ_enable_checkbox = QCheckBox("Enable EQ")
        self.EQ_enable_checkbox.setChecked(True)
        self.EQ_enable_checkbox.stateChanged.connect(self.EQ_enable_checkbox_toggled)

        self.EQ_label = QLabel("Equalizer enabled")

        self.EQ_select = QComboBox()
        self.EQ_select.addItems(["Custom", "Pop", "Rock", "Jazz", "Movie"])
        self.EQ_select.currentTextChanged.connect(self.EQ_modes_selection_changed)

        self.EQ_master_slider_label = QLabel("MASTER")
        self.EQ_low_slider_label = QLabel("LOW")
        self.EQ_mid_slider_label = QLabel("MID")
        self.EQ_high_slider_label = QLabel("HIGH")

        self.EQ_master_slider = QSlider(Qt.Vertical)
        self.EQ_master_slider.setMinimum(0)
        self.EQ_master_slider.setMaximum(100)
        self.EQ_master_slider.setValue(100)
        self.EQ_low_slider = QSlider(Qt.Vertical)
        self.EQ_low_slider.setMinimum(-20)
        self.EQ_low_slider.setMaximum(20)
        self.EQ_mid_slider = QSlider(Qt.Vertical)
        self.EQ_mid_slider.setMinimum(-20)
        self.EQ_mid_slider.setMaximum(20)
        self.EQ_high_slider = QSlider(Qt.Vertical)
        self.EQ_high_slider.setMinimum(-20)
        self.EQ_high_slider.setMaximum(20)

        self.EQ_master_slider_val_label = QLabel("100")
        self.EQ_low_slider_val_label = QLabel("0dB")
        self.EQ_mid_slider_val_label = QLabel("0dB")
        self.EQ_high_slider_val_label = QLabel("0dB")

        self.EQ_master_slider.valueChanged.connect(lambda: [self.EQ_master_slider_val_label.setText(str(self.EQ_master_slider.value())), self.player.setVolume(int(self.EQ_master_slider.value()))])
        self.EQ_low_slider.valueChanged.connect(lambda: self.EQ_low_slider_val_label.setText(str(self.EQ_low_slider.value()) + "dB"))
        self.EQ_mid_slider.valueChanged.connect(lambda: self.EQ_mid_slider_val_label.setText(str(self.EQ_mid_slider.value()) + "dB"))
        self.EQ_high_slider.valueChanged.connect(lambda: self.EQ_high_slider_val_label.setText(str(self.EQ_high_slider.value()) + "dB"))

        self.EQ_mode_bass_boosted = QRadioButton("Bass Booster")
        self.EQ_mode_bass_boosted.modename = "Bass Booster"
        self.EQ_mode_bass_boosted.toggled.connect(self.EQ_bass_mode_selected)

        self.EQ_mode_normal = QRadioButton("Normal")
        self.EQ_mode_normal.setChecked(True)
        self.EQ_mode_normal.modename = "Normal"
        self.EQ_mode_normal.toggled.connect(self.EQ_bass_mode_selected)

        self.layout_EQ.addWidget(self.EQ_enable_checkbox, 0, 0, 1, 4, alignment=Qt.AlignTop)
        self.layout_EQ.addWidget(self.EQ_label, 1, 0, 1, 4)
        self.layout_EQ.addWidget(self.EQ_select, 2, 0, 1, 4)

        self.layout_EQ.addWidget(self.EQ_master_slider_label, 3, 0)
        self.layout_EQ.addWidget(self.EQ_low_slider_label, 3, 1)
        self.layout_EQ.addWidget(self.EQ_mid_slider_label, 3, 2)
        self.layout_EQ.addWidget(self.EQ_high_slider_label, 3, 3)

        self.layout_EQ.addWidget(self.EQ_master_slider, 4, 0)
        self.layout_EQ.addWidget(self.EQ_low_slider, 4, 1)
        self.layout_EQ.addWidget(self.EQ_mid_slider, 4, 2)
        self.layout_EQ.addWidget(self.EQ_high_slider, 4, 3)

        self.layout_EQ.addWidget(self.EQ_master_slider_val_label, 5, 0)
        self.layout_EQ.addWidget(self.EQ_low_slider_val_label, 5, 1)
        self.layout_EQ.addWidget(self.EQ_mid_slider_val_label, 5, 2)
        self.layout_EQ.addWidget(self.EQ_high_slider_val_label, 5, 3)

        self.layout_EQ.addWidget(self.EQ_mode_bass_boosted, 6, 0, 1, 2)
        self.layout_EQ.addWidget(self.EQ_mode_normal, 6, 2, 1, 2)

        self.layout_main.addWidget(self.group_EQ, 1, 6)

        # theme / stay on top
        self.theme_checkbox = QCheckBox("Dark-Mode")
        self.theme_checkbox.stateChanged.connect(self.theme_checkbox_toggled)
        self.theme_checkbox.setChecked(True)
        self.theme_checkbox_toggled()

        self.window_on_top_checkbox = QCheckBox("Keep Window on Top")
        self.window_on_top_checkbox.stateChanged.connect(self.window_on_top_checkbox_toggled)
        self.window_on_top_checkbox.setChecked(True)
        self.window_on_top_checkbox_toggled()

        self.layout_main.addWidget(self.theme_checkbox, 2, 6, 1, 2, alignment=Qt.AlignLeft)
        self.layout_main.addWidget(self.window_on_top_checkbox, 3, 6, 1, 2, alignment=Qt.AlignLeft)


if __name__ == '__main__':

    songs = Song.load_songs_from_file_as_objects()

    app = QApplication([])
    window = MainWindow()
    app.exec_()

