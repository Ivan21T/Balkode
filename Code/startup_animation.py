import sys, os, vlc
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer, Qt, QRect
from PySide6.QtGui import QPainterPath, QRegion, QPalette, QColor
from activity_bar import base_dir


class RoundedVideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

    def resizeEvent(self, event):
        radius = 25
        path = QPainterPath()
        path.addRoundedRect(QRect(0, 0, self.width(), self.height()), radius, radius)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))
        super().resizeEvent(event)


class StartupAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 500)

        self.video_widget = RoundedVideoWidget(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.video_widget)

        self.instance = vlc.Instance("--quiet", "--no-xlib", "--no-video-title-show", "--intf", "dummy", "--no-audio")
        self.player = self.instance.media_player_new()
        self._embed_video_surface()

        video_path = os.path.join(base_dir, "Assets", "loader.mp4")
        media = self.instance.media_new(video_path)
        self.player.set_media(media)
        self.player.video_set_aspect_ratio("1:1")

        QTimer.singleShot(500, self.play_video)

        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_state)
        self.check_timer.start(1000)

    def _embed_video_surface(self):
        win_id = int(self.video_widget.winId())
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(win_id)
        elif sys.platform == "win32":
            self.player.set_hwnd(win_id)
        elif sys.platform == "darwin":
            self.player.set_nsobject(win_id)

    def play_video(self):
        if self.player:
            self.player.play()

    def check_state(self):
        if not self.player:
            return
        try:
            state = self.player.get_state()
            if state in (vlc.State.Ended, vlc.State.Error):
                self.cleanup()
        except Exception as e:
            self.cleanup()

    def cleanup(self):
        self.check_timer.stop()
        try:
            if self.player:
                self.player.stop()
                self.player.release()
                self.player = None
            if self.instance:
                self.instance.release()
                self.instance = None
        except Exception as e:
            print("Cleanup exception:", e)
        self.close()

    def closeEvent(self, event):
        self.cleanup()
        super().closeEvent(event)
