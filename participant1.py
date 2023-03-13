import time,coordinator,multiprocessing

if __name__ == '__main__':
    # TEST CASE ONE
    print('CASE ONE: ALL PARTRICIPANTS VOTE_COMMIT')
    obj = coordinator.twoPhaseCommit(0,1,0)
    p6 = []
    p6.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p6.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p6[::-1]:
        item.start()
    for item in p6:
        item.join(timeout = 50)
    for item in p6:
        item.terminate()
    print('-----------------------------------------------------------------------------------------------------------------------------------')


   
    # TEST CASE TWO
    print('CASE TWO: ONE OF THE PARTICIPANT VOTE_ABORT')
    obj = coordinator.twoPhaseCommit(0,2,1)
    p7 = []
    p7.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p7.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p7[::-1]:
        item.start()
    for item in p7:
        item.join(timeout = 10)
    for item in p7:
        item.terminate()
    time.sleep(35)

    print('------------------------------------------------------------------------------------------------------------------------------------')


    # TEST CASE THREE
    print('CASE THREE: COORDINATOR SENDING REQUEST MESSAGE TO PARTICIPANTS TO COMMIT AND FAILS')
    obj = coordinator.twoPhaseCommit(0,3,1)
    p8 = []
    p8.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p8.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p8[::-1]:
        item.start()
    for item in p8:
        item.join(timeout = 90)
    for item in p8:
        item.terminate()
    print('------------------------------------------------------------------------------------------------------------------------------------')


    # TEST CASE FOUR
    print('CASE FOUR: COORDINATOR FAILS AFTER SENDING COMMIT MESSAGE')

    obj = coordinator.twoPhaseCommit(0,4,2)
    p9 = []
    p9.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p9.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p9[::-1]:
        item.start()
    for item in p9:
        item.join(timeout = 90)
    for item in p9:
        item.terminate()
        
    print('-------------------------------------------------------------------------------------------------------------------------------------')





