import multiprocessing,socket,struct,marshal,time

IP = '224.1.1.1'
PORT = 6005
MULTICAST = 2

class twoPhaseCommit:
    def __init__(self,id,caseNumber,value,phase = None):
        self.id = id
        self.validList = [0,0,0]
        self.value = value
        self.updatedValue = value
        self.caseNumber = caseNumber
        self.acknowledgements = 0
        self.phase = phase

    ## Function to send the messages to the particular participants

    def sendMsg(self,message = None):
       
        ################################ UDP Socket #########################################
        socketSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        socketSend.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST)
        #Checking for the test cases where coordinator didn't fail
        if self.id == 'coordinator' and message == None and self.phase == None and (self.caseNumber == 1 or self.caseNumber == 2 or self.caseNumber==4):
            #Have used dictionary structure to append the message and the participants requests
                message = {"PID": str(self.id),"data": 'Checking if Participant P' + str(self.id)+ 'wants to Commit the Transaction',"request": 'check',}
                self.validList = [0,0,0]
                #serializing the sent message into byte
                message = marshal.dumps(message)
                socketSend.sendto(message, (IP, PORT))
                # Restart the coordinator when it sends an request it can commit
        elif self.id == 'coordinator' and message == None and self.phase == 'start2PC'and (self.caseNumber == 3 or self.caseNumber==4):
                #Requesting previous log data
                message = {"PID": str(self.id),"data": 'Cordinator C1 requesting the log data',"request": 'log',}
                self.validList = [0, 0, 0]
                message = marshal.dumps(message)
                socketSend.sendto(message, (IP, PORT))
        elif message!=None:
            message = marshal.dumps(message)
            socketSend.sendto(message, (IP, PORT))
            print(marshal.loads(message))

   ## Function for receiving the failure testcases rquests along with the partcipant idd andits message requests         

    def recMsg(self):
        socketRec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        socketRec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
        socketRec.bind((IP, PORT))
        messageRequest = struct.pack("=4sl", socket.inet_aton(IP), socket.INADDR_ANY)
        socketRec.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, messageRequest)
        while True:
            data ,address = socketRec.recvfrom(10240)
            data = marshal.loads(data)
            request = data['request']
            req_data = data["PID"]
             
             # When participant aborts
            if self.caseNumber == 2 and self.acknowledgements == 2 and self.id == 'coordinator':
                time.sleep(10)

                #sending the kill request type and aborting the particular transaction
                data_to_be_sent = {"PID": str(self.id),"data": 'Coordinator C1 sending message to participant P' + str(self.id) + 'to Abort',"request": 'kill',"message": "VOTE_ABORT",}
                print(' Aborted !  :', self.value)
                self.validList = [0, 0, 0]
                self.sendMsg(data_to_be_sent)
                time.sleep(20)
            if req_data != 'coordinator' and request == 'Ack' and self.id =='coordinator':
                self.acknowledgements +=1
            if req_data !='coordinator' and int(req_data) != self.id:
                print(data)
            if request == 'check' and req_data == 'coordinator' and self.id != 'coordinator':
                if self.caseNumber == 1 or self.caseNumber == 2 or self.caseNumber==4:
                    self.updatedValue = self.value + 1

                    print('value before calculation:',self.value)
                    #once a partcipant commits we update here
                    print('value after calculation:',self.updatedValue)
                data_to_be_sent = {"PID": str(self.id),"data": 'participant P' +str(self.id)+' sending message regrading commit request',"request": 'Ack',"message":'Yes!',}
                self.sendMsg(data_to_be_sent)
            elif (request == 'Commit' or request == 'kill') and self.id != 'coordinator':
                if request == 'Commit':
                    self.value = self.updatedValue
                    print('Transaction request Committed! :',self.value)
                else:

                    #test case 3 where coordinator  recovers
                    if self.id == 0 and self.caseNumber == 3:
                        print('--------------Cordinator C1  is recovered after the ready message and it is recovering data from participants--------------')
                    print('Aborted!:',self.value)
            elif request == 'Ack' and self.id == 'coordinator':
                self.validList[int(req_data)] = data["message"]
                if 0 not in self.validList:
                    if 'N' not in self.validList:
                        data_to_be_sent = {"PID": str(self.id),"data": 'Coordinator C1 sending message to commit',"request": 'Commit',"message": "VOTE_COMMIT",}
                        self.value +=1
                        if self.caseNumber !=4:
                            print('Transaction request Committed!:', self.value)
                    else:
                        data_to_be_sent = {"PID": str(self.id),"data": 'Coordinator C1 sending message to Abort',"request": 'kill',"message": "VOTE_ABORT",}
                        print('Transaction Aborted!:', self.value)
                    self.validList = [0,0,0]
                    self.sendMsg(data_to_be_sent)
            elif request == 'log' and self.id == 1:
                data_to_be_sent = {"PID": str(self.id),"data": 'The participant P' + str(self.id)+ 'sending log data to Coordinator C1 ',"request": 'backup_data',"message": self.value,}
                self.sendMsg(data_to_be_sent)
                #requested for  backup data 
            elif request == 'backup_data' and self.id == 'coordinator':    
                data_to_be_sent = {"PID": str(self.id),"data": 'Coordinator C1 sending message to to commit',"request": 'Commit',"message": "VOTE_COMMIT",}
                self.value = int(data['message'])

                # Total committed Participants
                print('Final Commits done!:', self.value)
                if self.caseNumber != 4:
                    self.sendMsg(data_to_be_sent)


def testcase():
   # IN TEST CASE ONE ALL PARTICIPANTS VOTE WILL BE COMMITED TO COORDINATOR
    print('CASE ONE: ALL PARTICIPANTS VOTE_COMMIT')
    obj = twoPhaseCommit('coordinator',1,0)
    p = []
    p.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p[::-1]:
        item.start()
    for item in p:
        item.join(timeout = 50)
    for item in p:
        item.terminate()
    print('--------------------------------------------------------------------------------------------------')
   
   # IN TEST CASE TWO PARTICIPANT ONE WILL ABORT FROM VOTING CAUSING COORDINATOR TO CONSIDER THE VALUES OF THE NEXT TWO PARTICIPANTS
    print('CASE TWO: ONE OF THE PARTICIPANT VOTE_ABORT')
    time.sleep(10)
    p1 = []
    obj = twoPhaseCommit('coordinator',2,1)
    p1.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p1.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p1[::-1]:
        item.start()
    for item in p1:
        item.join(timeout = 50)
    for item in p1:
        item.terminate()
    print('----------------------------------------------------------------------------------------------------')


    # IN TEST CASE THREE THE COORDINATOR REQUESTS TO SEND THE COMMIT MESSAGE TO PARTICIPANTS AND FAILS 
    print('CASE THREE: COORDINATOR REQUESTS TO SEND THE COMMIT MESSAGE TO PARTICIPANTS AND FAILS ')
    obj = twoPhaseCommit('coordinator',3,1)
    p2 = []
    p2.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p2.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p2[::-1]:
        item.start()
    for item in p2:
        item.join(timeout = 20)
    for item in p2:
        item.terminate()    

    obj = twoPhaseCommit('coordinator',3,1,'start2PC')  #restarts
    p3 = []
    p3.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p3.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p3[::-1]:
        item.start()
    for item in p3:
        item.join(timeout = 20)
    for item in p3:
        item.terminate()
    time.sleep(35)
    print('-----------------------------------------------------------------------------------------------------')


   #IN TEST CASE FOUR COORDINATOR FAILS AFTER SENDING COMMIT MESSAGE
    print('CASE FOUR: COORDINATOR FAILS AFTER SENDING COMMIT MESSAGE')
    obj = twoPhaseCommit('coordinator',4,2)
    p4 = []
    p4.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p4.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p4[::-1]:
        item.start()
    for item in p4:
        item.join(timeout = 30)
    for item in p4:
        item.terminate()

    obj = twoPhaseCommit('coordinator',4,2,'start2PC')     #Recovering
    p5 = []
    p5.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p5.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p5[::-1]:
        item.start()
    for item in p5:
        item.join(timeout = 50)
    for item in p5:
        item.terminate()

    print('---------------------------------------------------------------------------------------------------------')



if __name__=='__main__':
    testcase()

