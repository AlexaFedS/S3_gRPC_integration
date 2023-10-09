from __future__ import print_function

import logging
import io

import grpc
import grpc_server_pb2
import grpc_server_pb2_grpc

def test_getList(stub, name):
    listFile = stub.GetList(name)
    print('List got')
    for c in listFile:
        print(c.title)

def test_addFile(stub, file):
    status = stub.AddFile(file)
    print(status.status)
    if not status.status:
        print(status.error_message)

def test_getFile(stub, file):
    inFile = stub.GetFile(file)
    #ourFile=io.StringIO(inFile).read().encode('latin-1')
    #with open(file.title, 'wb') as f:
    #    f.write(ourFile)
    print('File got ', inFile)

def test_editFile(stub, file):
    status = stub.EditFile(file)
    print(status.status)
    if not status.status:
        print(status.error_message)

def test_deleteFile(stub, file):
    status= stub.DeleteFile(file)
    print(status.status)
    if not status.status:
        print(status.error_message)


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = grpc_server_pb2_grpc.ServerMethodsStub(channel)
        #test_getList(stub, grpc_server_pb2.BucketName(name = 'articles'))
        #file = io.FileIO('6.pdf', 'rb').read()
        #test_addFile(stub, grpc_server_pb2.FileRequest(bucketName='articles', title='Лаб6.pdf', content = file.decode('latin-1'), contentType='application/pdf'))
        #test_getFile(stub, grpc_server_pb2.FileName(bucketName = 'articles', title = '1.pdf'))
        #test_editFile(stub, grpc_server_pb2.FileRequest(bucketName='articles', title='Документ1.pdf', content = file.decode('latin-1'), contentType='application/pdf'))
        test_deleteFile(stub, grpc_server_pb2.FileName(bucketName='articles', title = 'Лаб6.pdf'))
        channel.close

if __name__ == "__main__":
    logging.basicConfig()
    run()