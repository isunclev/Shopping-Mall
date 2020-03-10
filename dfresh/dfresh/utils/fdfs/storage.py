from django.core.files.storage import Storage
from fdfs_client.client import *
from django.conf import settings


class FDFSStorage(Storage):
    '''fdfs文件存储类'''
    def __init__(self, client_conf=None, base_url=None):
        if client_conf == None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url == None:
            base_url = settings.FDFS_STORAGE_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        trackers = get_tracker_conf(self.client_conf)
        client = Fdfs_client(trackers)

        res = client.upload_by_buffer(content.read())

        if res.get('Status') != 'Upload successed.':
            raise Exception('upload file to fdfs failed.')

        filename = res.get('Remote file_id')
        return filename.decode()

    def exists(self, name):
        return False

    def url(self, name):
        return self.base_url + name