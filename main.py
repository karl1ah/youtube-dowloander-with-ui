import os
import re
import moviepy.editor as mp
from pytube import YouTube, Playlist
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QFileDialog

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(100, 100, 800, 300)

        self.playlist_label = QLabel('Playlist URL:', self)
        self.playlist_label.move(20, 20)
        self.playlist_input = QLineEdit(self)
        self.playlist_input.move(110, 20)
        self.playlist_input.resize(500, 20)

        self.video_label = QLabel('Video URL:', self)
        self.video_label.move(20, 60)
        self.video_input = QLineEdit(self)
        self.video_input.move(110, 60)
        self.video_input.resize(500, 20)

        self.download_button = QPushButton('Download', self)
        self.download_button.move(400, 100)
        self.download_button.clicked.connect(self.download)

        self.file_type_label = QLabel('File type:', self)
        self.file_type_label.move(20, 140)
        self.file_type_combo = QComboBox(self)
        self.file_type_combo.addItem('mp3')
        self.file_type_combo.addItem('mp4')
        self.file_type_combo.move(110, 140)

        self.resolution_label = QLabel('Resolution:', self)
        self.resolution_label.move(20, 180)
        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItem('144p')
        self.resolution_combo.addItem('240p')
        self.resolution_combo.addItem('360p')
        self.resolution_combo.addItem('480p')
        self.resolution_combo.addItem('720p')
        self.resolution_combo.addItem('1080p')
        self.resolution_combo.addItem('1440p')
        self.resolution_combo.addItem('2160p')
        self.resolution_combo.move(110, 180)

        self.show()

    def download(self):
        playlist_url = self.playlist_input.text()
        video_url = self.video_input.text()
        file_type = self.file_type_combo.currentText()
        resolution = self.resolution_combo.currentText()

        # YouTube linklerinin formatına uygun bir desen tanımla
        pattern = r"https?://www\.youtube\.com/(watch|playlist)\?(\w+)=(\w+)"

        if playlist_url:
            # Cümleyi desenle eşleştir
            match = re.search(pattern, playlist_url)
            # Eşleşme varsa
            if match and match.group(1) == "playlist":
                # Playlist nesnesini oluşturun
                playlist = Playlist(playlist_url)
                # Playlist içindeki her video için işlemleri gerçekleştirin
                for video in playlist.videos:
                    self.download_video(video, file_type, resolution)
            else:
                QMessageBox.critical(self, 'Error', 'Please enter a valid YouTube playlist URL.')
        elif video_url:
            # Cümleyi desenle eşleştir
            match = re.search(pattern, video_url)
            # Eşleşme varsa
            if match and match.group(1) == "watch":
                # YouTube nesnesini oluşturun ve videoyu indirin
                yt = YouTube(video_url)
                self.download_video(yt, file_type, resolution)
            else:
                QMessageBox.critical(self, 'Error', 'Please enter a valid YouTube video URL.')
        else:
            QMessageBox.critical(self, 'Error', 'Please enter a YouTube playlist URL or video URL.')

    def download_video(self, video, file_type, resolution):
        # İstenen akışı bulun ve indirin
        if file_type == 'mp3':
            stream = video.streams.filter(only_audio=True).first()
            extension = 'mp3'
        else:
            stream = video.streams.filter(file_extension='mp4', res=resolution).first()
            extension = 'mp4'

        if stream is not None:
            print(f"Downloading: {video.title}")
            stream.download()

            # Eğer sadece ses indirildiyse, indirme işleminden önce ses olarak dönüştürün
            if file_type == 'mp3':
                input_path = os.path.join(os.getcwd(), video.title + ".mp4")
                output_path = os.path.join(os.getcwd(), video.title + ".mp3")
                clip = mp.AudioFileClip(input_path)
                clip.write_audiofile(output_path)

                clip.close()
                os.remove(input_path) # mp4 dosyasını siler

            QMessageBox.information(self,'Information', f'{video.title} indirmesi tamamlandı.')
        else:
            QMessageBox.critical(self, 'Error', f'indirme hatası {video.title}. Please check the file type and resolution.')

if __name__ == '__main__':
    app = QApplication([])
    window = YouTubeDownloader()
    app.exec_()