import coordinator,multiprocessing

if __name__ == '__main__':
    # TEST CASE  ONE
    print('CASE ONE: ALL PARTICIPANTS VOTE_COMMIT')
    obj = coordinator.twoPhaseCommit(1,1,0)
    p10 = []
    p10.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p10.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p10[::-1]:
        item.start()
    for item in p10:
        item.join(timeout = 50)
    for item in p10:
        item.terminate()

    print('---------------------------------------------------------------------------------------------------------------------------')


    # TEST CASE TWO
    print('CASE TWO: ONE OF THE PARTICIPANT VOTE_ABORT')
    obj = coordinator.twoPhaseCommit(1,2,1)
    p11 = []
    p11.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p11.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p11[::-1]:
        item.start()
    for item in p11:
        item.join(timeout = 50)
    for item in p11:
        item.terminate()

    print('----------------------------------------------------------------------------------------------------------------------------')

    # TEST CASE THREE
    print('CASE THREE: COORDINATOR SENDING REQUEST COMMIT MESSAGE TO PARTICIPANTS AND FAILS')
    obj = coordinator.twoPhaseCommit(1,3,1)
    p12 = []
    p12.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p12.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p12[::-1]:
        item.start()
    for item in p12:
        item.join(timeout = 90)
    for item in p12:
        item.terminate()

    print('-------------------------------------------------------------------------------------------------------------------------------')


    # TEST CASE FOUR
    print('CASE FOUR: COORDINATOR FAILS AFTER SENDING COMMIT MESSAGE')
    obj = coordinator.twoPhaseCommit(1,4,2)
    p13 = []
    p13.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p13.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p13[::-1]:
        item.start()
    for item in p13:
        item.join(timeout = 90)
    for item in p13:
        item.terminate()
    print('---------------------------------------------------------------------------------------------------------------------------------')

