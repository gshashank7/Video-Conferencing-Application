


import cv2
import socket
import pickle
import struct
# from threading import Thread as worker
from multiprocessing import Process as worker


def sendData(serverPort, serverIP):
    '''
    :param serverPort: The port number of server to send video packets to.
    :param serverIP: The IP address of the server.
    :return:  None

    This method takes in the server ip address and port number as arguments , creates a socket and sends the frame captured
    by web camera through that socket
    '''
    cap = cv2.VideoCapture(0)
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((serverIP, serverPort))
    while True:
        ret, frame = cap.read()
        ret = cap.set(3, 150)
        ret = cap.set(4, 150)
        data = pickle.dumps(frame)  ### new code
        print("data sent1")
        # print(type(data))
        clientsocket.sendall(struct.pack("i", len(data)) + data)  ### new code
        print("data sent2")


def recvData(clientPort):
    '''
    :param clientPort:  The port number of the client from which the data is being received
    :return: None

    This method receives the data and stores it in a buffer. Once the entire frame has been received, the frame is loaded back from pickle
    file and displayed in the window using a method from openCV called imshow
    '''
    HOST = ''
    PORT = clientPort
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket created')
    s.bind((HOST, PORT))
    print ('Socket bind complete')
    s.listen(10)
    print ('Socket now listening')

    conn, addr = s.accept()
    print("Conn successful")
    ### new
    data = ""
    payload_size = struct.calcsize("i")


    while True:

        while len(data) < payload_size:
            data += str(conn.recv(4096))
        data = str(data)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        # packed_msg_size = str.encode(packed_msg_size)
        msg_size = struct.unpack("i", packed_msg_size)[0]
        while len(data) < msg_size:
            data += str(conn.recv(4096))
        frame_data = data[:msg_size]
        data = data[msg_size:]
        ###


        frame = pickle.loads(frame_data)
        # print(frame)
        print (clientPort)



        cv2.imshow(str(clientPort), frame)
        cv2.waitKey(1)






def main():
    '''

    Two threads are started for receive data and the send data is called by main thread.
    '''
    port = [8001, 9001]
    t = []
    # serverPort = int(input("Enter server port:"))
    # serverIP = input("Enter server ip:")

    # thread.start_new_thread(recvData, (port[0],))
    # thread.start_new_thread(recvData, (port[1],))

    t.append(worker(target=recvData,args = (port[0],)))
    t.append(worker(target=recvData, args= (port[1],)))

    t[0].start()
    t[1].start()

    sendData(6001, '129.21.120.158')



if __name__ == '__main__':
    main()



