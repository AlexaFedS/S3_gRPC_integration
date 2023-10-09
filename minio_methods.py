from minio import Minio
from minio.error import S3Error
from config import Config
import io


class MinioClass:
    def __init__(self):
        try:
            self.config = Config('minio_config.cfg')
            self.client = Minio(endpoint=self.config['socket'],
                                access_key=self.config['access_key'],
                                secret_key=self.config['secret_key'],
                                secure=False)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def __del__(self):
        print('minio connection closed')

    def add_file(self, name: str, title: str, content, c_type):
        file_io_object = io.StringIO(content)
        b_content = file_io_object.read().encode('latin-1')
        try:
            result = self.client.put_object(bucket_name=name,
                                            object_name=title,
                                            data=io.BytesIO(b_content),
                                            length=len(b_content),
                                            content_type=c_type)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def get_files_list(self, name: str):
        list_of_titles = []
        try:
            file_list = self.client.list_objects(bucket_name=name)
            for file in file_list:
                list_of_titles.append(file.object_name)
            return list_of_titles
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def get_file(self, name: str, title: str):
        try:
            if(name == 'articles'):
                file = f'http://127.0.0.1:9000/articles/{title}'
            else:
                file = f'http://127.0.0.1:9000/authors/{title}'
            return file
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def remove_file(self, name:str, title:str):
        try:
            result = self.client.remove_object(bucket_name=name, object_name=title)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)