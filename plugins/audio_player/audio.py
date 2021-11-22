import sys, os
from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QFileDialog
from PySide2.QtCore import QUrl, QDir
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent

class AudioWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Kreitanje layout-a

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.playBtn = QPushButton("Play", clicked=self.openFile)
        self.layout.addWidget(self.playBtn)

        volumeControl = QHBoxLayout()
        self.layout.addLayout(volumeControl)

        # Kreiranje ostalih widget-a

        btnVolumeUp = QPushButton("+", clicked=self.volumeUp)
        btnVolumeDown = QPushButton("-", clicked=self.volumeDown)
        butVolumeMute = QPushButton("Mute", clicked=self.volumeMute)

        volumeControl.addWidget(btnVolumeUp)
        volumeControl.addWidget(btnVolumeDown)
        volumeControl.addWidget(butVolumeMute)

        self.player = QMediaPlayer()

        self.current_volume = self.player.volume()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Audio",
                QDir.homePath())

        if fileName != '':
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.player.play()

    def volumeUp(self):
        print("Volume pre poglasnjavanja " + str(self.current_volume))
        self.player.setVolume(self.current_volume + 5)
        print("Volume posle poglasnjavanja " + str(self.current_volume))

    def volumeDown(self):
        print("Volume pre utisavanja " + str(self.current_volume))
        self.player.setVolume(self.current_volume - 5)
        print("Volume posle utisavanja " + str(self.current_volume))

    def volumeMute(self):
        self.player.setMuted(not self.player.isMuted())
