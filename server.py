from concurrent import futures
import logging

import grpc
import grpc_server_pb2
import grpc_server_pb2_grpc
from minio_methods import MinioClass

class gRPCServer(grpc_server_pb2_grpc.ServerMethodsServicer):
    def __init__(self):
        try:
            self.minio = MinioClass()
        except ConnectionError:
            print('Connection failed')
        except Exception as e:
            print('Unknown error ', e)
        else:
            print('Connection succeed')

    def GetList(self, request, context):
        print('Request: GetList')
        try:
            file_list = self.minio.get_files_list(request.name)
            for file in file_list:
                print(file)
                yield grpc_server_pb2.ListResponse(title=file)
        except Exception as e:
            print(e)

    def GetFile(self, request, context):
        print('Request: GetFile')
        try:
            file = self.minio.get_file(request.bucketName, request.title)
            return grpc_server_pb2.File(content = file)
        except Exception as e:
            print(e)

    def AddFile(self, request, context):
        print('Request: AddFile')
        try:
            self.minio.add_file(request.bucketName, request.title, request.content, request.contentType)
        except ValueError as ve:
            status = grpc_server_pb2.Status(status=400)
            print(ve)
        except ConnectionError:
            status = grpc_server_pb2.Status(status=500)
        except Exception as e:
            status = grpc_server_pb2.Status(status=500)
            print(e)
        else:
            status = grpc_server_pb2.Status(status=200)
        return status
    
    def EditFile(self, request, context):
        print('Request: EditFile')
        try:
            if request.title is not None:
                self.minio.remove_file(request.bucketName, request.title)
            self.minio.add_file(request.bucketName, request.title, request.content, request.contentType)
        except ValueError:
            status = grpc_server_pb2.Status(status=400)
        except ConnectionError as e:
            status = grpc_server_pb2.Status(status=500)
            print(e)
        except Exception as e:
            status = grpc_server_pb2.Status(status=500)
            print(e)
        else:
            status = grpc_server_pb2.Status(status=200)
        return status
    
    def DeleteFile(self, request, context):
        print('Request: DeleteFile')
        try:
            self.minio.remove_file(request.bucketName, request.title)
        except ValueError:
            status = grpc_server_pb2.Status(status=400)
        except ConnectionError:
            status = grpc_server_pb2.Status(status=500)
        except Exception:
            status = grpc_server_pb2.Status(status=500)
        else:
            status = grpc_server_pb2.Status(status=200)
        return status
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_server_pb2_grpc.add_ServerMethodsServicer_to_server(gRPCServer(), server)
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    server.add_insecure_port('0.0.0.0:30000')
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
