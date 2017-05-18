from configparser import ConfigParser
import CommonUtil
import os


CONFIG_WEB = 0
CONFIG_APP = 1


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            return cls.__instance


class ConfigManager(metaclass=Singleton):
    def __init__(self):
        self.cfg_web = ConfigParser()
        self.cfg_web.read(os.path.join(CommonUtil.resource_abs_path(), 'config_web.ini'))

        self.cfg_app = ConfigParser()
        self.cfg_app.read(os.path.join(CommonUtil.resource_abs_path(), 'config_app.ini'))

    def config_instance(self, config_type):
        if config_type == CONFIG_WEB:
            return self.cfg_web
        else:
            return self.cfg_app

    def main_w(self, config_type):
        return self.config_instance(config_type).getint('main', 'w')

    def main_h(self, config_type):
        return self.config_instance(config_type).getint('main', 'h')

    def tag_x(self, config_type):
        return self.config_instance(config_type).getint('tag', 'x')

    def tag_y(self, config_type):
        return self.config_instance(config_type).getint('tag', 'y')

    def tag_h(self, config_type):
        return self.config_instance(config_type).getint('tag', 'h')

    def tag_font(self, config_type):
        return self.config_instance(config_type).get('tag', 'font')

    def tag_font_size(self, config_type):
        return self.config_instance(config_type).getint('tag', 'font_size')

    def desc_x(self, config_type):
        return self.config_instance(config_type).getint('desc', 'x')

    def desc_b(self, config_type):
        return self.config_instance(config_type).getint('desc', 'b')

    def desc_max_width(self, config_type):
        return self.config_instance(config_type).getint('desc', 'max_width')

    def desc_line_spacing(self, config_type):
        return self.config_instance(config_type).getint('desc', 'line_spacing')

    def desc_font(self, config_type):
        return self.config_instance(config_type).get('desc', 'font')

    def desc_font_size(self, config_type):
        return self.config_instance(config_type).getint('desc', 'font_size')

    def title_x(self, config_type):
        return self.config_instance(config_type).getint('title', 'x')

    def title_bottom_spacing_to_desc_y(self, config_type):
        return self.config_instance(config_type).getint('title', 'bottom_spacing_to_desc_y')

    def title_max_width(self, config_type):
        return self.config_instance(config_type).getint('title', 'max_width')

    def title_line_spacing(self, config_type):
        return self.config_instance(config_type).getint('title', 'line_spacing')

    def title_font(self, config_type):
        return self.config_instance(config_type).get('title', 'font')

    def title_font_size(self, config_type):
        return self.config_instance(config_type).getint('title', 'font_size')