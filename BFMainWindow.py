from PyQt5.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QAction, \
    QFileDialog, QSizePolicy, QMessageBox  # , QInputDialog
from PyQt5.QtGui import QKeySequence, QPixmap, QColor
from PyQt5.QtCore import Qt
import ImageProcess
from PIL import Image, ImageQt
import os
from Error import IrregularError


items = ['标签', '标题', '描述']
tag_types = ['专题', '活动', '签约作者', '热点']


# noinspection PyUnresolvedReferences,PyArgumentList
class BFMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.opened_image_path = None
        self.opened_image = None
        self.processed_image = None

        self.image_view = QLabel()
        self.image_view.setStyleSheet('QLabel { background-color : black; }')
        self.image_view.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_view.setAlignment(Qt.AlignCenter)

        self.combo_box = QComboBox()
        self.combo_box.addItems(tag_types)
        for i in range(len(tag_types)):
            self.combo_box.setItemData(i, QColor(*(ImageProcess.TAG_COLOR_LIST[i])), Qt.ForegroundRole)

        self.tag_edit = QLineEdit()
        self.title_edit = QLineEdit()
        self.desc_edit = QLineEdit()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('BannerFactory')
        self.resize(540, 480)
        self.setMinimumSize(540, 480)
        self.setup_menu()
        self.setup_main()

    def setup_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('文件')

        open_local_action = QAction('打开图片…', self)
        open_local_action.setShortcut(QKeySequence.Open)
        open_local_action.triggered.connect(self.open_local)
        file_menu.addAction(open_local_action)

        # search_image_action = QAction('搜索图片…', self)
        # search_image_action.setShortcut(QKeySequence.Find)
        # search_image_action.triggered.connect(self.search_remote_image)
        # file_menu.addAction(search_image_action)

        save_action = QAction('保存…', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)
        # ---------------------------------------
        function_menu = menu_bar.addMenu('功能')

        preview_action = QAction('预览', self)
        preview_action.setShortcut(Qt.CTRL + Qt.Key_P)
        preview_action.triggered.connect(self.preview)
        function_menu.addAction(preview_action)

    def setup_main(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_vbox = QVBoxLayout(central_widget)
        main_vbox.setContentsMargins(0, 0, 0, 0)

        image_box = QHBoxLayout()
        image_box.addWidget(self.image_view)
        main_vbox.addLayout(image_box)

        input_vbox = QVBoxLayout()
        input_vbox.setContentsMargins(20, 20, 20, 20)
        for item in items:
            hbox = QHBoxLayout()
            label = QLabel(item)
            hbox.addWidget(label)

            if item == '标签':
                hbox.addWidget(self.combo_box)
                hbox.addWidget(self.tag_edit)
            elif item == '标题':
                hbox.addWidget(self.title_edit)
            elif item == '描述':
                hbox.addWidget(self.desc_edit)

            input_vbox.addLayout(hbox)
        main_vbox.addLayout(input_vbox)

    def open_local(self):
        fname = QFileDialog.getOpenFileName(caption='打开图片',
                                            filter='Images (*.png *.jpg *.jpeg *.tiff *.bmp *.webp)',
                                            options=QFileDialog.DontResolveSymlinks)
        if fname[0]:
            self.processed_image = None
            self.opened_image_path = fname[0]

            self.opened_image = QPixmap(self.opened_image_path)
            self.scale_image_to_aspect_fit_label(self.opened_image)

    # def search_remote_image(self):
    #     text, ok = QInputDialog.getText(self, '搜索', '图片关键词：')
    #     if ok:
    #         pass

    def save(self):
        if self.processed_image is None:
            show_error_alert('请先预览图片生成效果', '预览后才能生成Banner图片')
            return

        fname = QFileDialog.getSaveFileName(caption='保存',
                                            options=QFileDialog.DontResolveSymlinks)
        if fname[0]:
            dir_name = os.path.dirname(fname[0])
            image_name = os.path.splitext(os.path.basename(fname[0]))[0]
            self.processed_image.save(os.path.join(dir_name, 'Web_' + image_name + '.jpg'),
                                      quality=ImageProcess.SAVE_IMAGE_QUALITY,
                                      optimize=True)

            processed_image_app = ImageProcess.process(1,
                                                       Image.open(self.opened_image_path),
                                                       self.tag_edit.displayText(),
                                                       self.title_edit.displayText(),
                                                       self.desc_edit.displayText(),
                                                       self.combo_box.currentIndex())
            processed_image_app.save(os.path.join(dir_name, 'App_' + image_name + '.jpg'),
                                     quality=ImageProcess.SAVE_IMAGE_QUALITY,
                                     optimize=True)

    def preview(self):
        error_message = None
        if self.opened_image_path is None:
            error_message = '请选择图片'
        elif len(self.tag_edit.displayText()) == 0:
            error_message = '请填写标签'
        elif len(self.title_edit.displayText()) == 0:
            error_message = '请填写标题'
        elif len(self.desc_edit.displayText()) == 0:
            error_message = '请填写描述'

        if error_message:
            show_error_alert('有未完成项目', error_message)
            return

        image = Image.open(self.opened_image_path)
        try:
            self.processed_image = ImageProcess.process(0,
                                                        image,
                                                        self.tag_edit.displayText(),
                                                        self.title_edit.displayText(),
                                                        self.desc_edit.displayText(),
                                                        self.combo_box.currentIndex())
            self.scale_image_to_aspect_fit_label(ImageQt.toqpixmap(self.processed_image))
        except IrregularError as e:
            show_error_alert('出错了', e.message)

    def resizeEvent(self, QResizeEvent):
        current_image = None
        if self.processed_image:
            current_image = ImageQt.toqpixmap(self.processed_image)
        elif self.opened_image:
            current_image = self.opened_image

        if current_image:
            self.scale_image_to_aspect_fit_label(current_image)

    def scale_image_to_aspect_fit_label(self, qpixmap):
        if qpixmap:
            scaled_image = qpixmap.scaled(self.image_view.size(), Qt.KeepAspectRatio | Qt.SmoothTransformation)
            self.image_view.setPixmap(scaled_image)


def show_error_alert(title, message):
    alert = QMessageBox()
    alert.setText(title)
    alert.setInformativeText(message)
    alert.setIcon(QMessageBox.Critical)
    alert.setStandardButtons(QMessageBox.Ok)
    alert.exec_()
