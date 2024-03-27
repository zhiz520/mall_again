from django.urls.converters import register_converter


class UsernameConverter:
    """自定义URL路径转换器"""
    regex = r"\w{5,20}"

    def to_python(self, value):
        return value