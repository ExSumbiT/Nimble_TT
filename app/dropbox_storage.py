import dropbox
from dropbox.exceptions import AuthError


class Storage:
    def __init__(self, access_token):
        try:
            dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        except AuthError as e:
            print('Error connecting to Dropbox with access token: ' + str(e))
        self.dbx = dropbox.Dropbox(access_token)

    def upload_file(self, binary_file_stream, file_to):
        """upload a file to Dropbox using API v2
        """

        # with open(file_from, 'rb') as f:
        # self.dbx.files_upload(f.read(), file_to)
        self.dbx.files_upload(binary_file_stream.read(), file_to)
