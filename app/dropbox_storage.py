import dropbox
from dropbox.exceptions import AuthError
from dotenv import dotenv_values

config = dotenv_values(".env")


class Storage:
    def __init__(self):
        try:
            self.dbx = dropbox.Dropbox(app_key=config['DROPBOX_APP_KEY'],
                                       app_secret=config['DROPBOX_APP_SECRET'],
                                       oauth2_refresh_token=config['DROPBOX_REFRESH_TOKEN'])
        except AuthError as e:
            print('Error connecting to Dropbox with access token: ' + str(e))

    def upload_file(self, binary_file_stream, path):
        """upload a file to Dropbox"""

        if self.dbx:
            self.dbx.files_upload(binary_file_stream, path)

    def download_file(self, path):
        """download file from Dropbox"""

        if self.dbx:
            meta, resp = self.dbx.files_download(path)
            return meta.name, resp.content
