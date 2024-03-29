from django.core.files.storage import Storage


class MyStorage(Storage):
    '''文件储存'''
    def _open(self, name, mode="rb"):
        pass

    def _save(self, name, content, max_length=None):
        pass

    def url(self, name):
        return 'http://192.168.5.97:8888' + name


