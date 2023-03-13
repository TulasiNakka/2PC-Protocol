import coordinator,multiprocessing

if __name__ == '__main__':
    # TEST CASE ONE
    print('CASE ONE: ALL PARTICIPANTS VOTE_COMMIT')
    obj = coordinator.twoPhaseCommit(2,1,0)
    p14 = []
    p14.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p14.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p14[::-1]:
        item.start()
    for item in p14:
        item.join(timeout = 50)
    for item in p14:
        item.terminate()
    
    print('-------------------------------------------------------------------------------------------------------------------------------')

    # TEST CASE TWO
    print('CASE TWO: ONE OF THE PARTICIPANT VOTE_ABORT')
    obj = coordinator.twoPhaseCommit(2,2,1)
    p15 = []
    p15.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p15.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p15[::-1]:
        item.start()
    for item in p15:
        item.join(timeout = 50)
    for item in p15:
        item.terminate()
    
    print('---------------------------------------------------------------------------------------------------------------------------------')

    # TETS CASE THREE
    print('CASE THREE: COORDINATOR SENDING REQUEST MESSAGE TO PARTCIPANTS AND FAILS')
    obj = coordinator.twoPhaseCommit(2,3,1)
    p16 = []
    p16.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p16.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p16[::-1]:
        item.start()
    for item in p16:
        item.join(timeout = 80)
    for item in p16:
        item.terminate()

    print('----------------------------------------------------------------------------------------------------------------------------------')



    # TEST CASE FOUR
    print('CASE FOUR: COORDINATOR FAILS AFTER SENDING COMMIT MESSAGE')

    obj = coordinator.twoPhaseCommit(2,4,2)
    p17 = []
    p17.append(multiprocessing.Process(target=obj.sendMsg, args=()))
    p17.append(multiprocessing.Process(target=obj.recMsg, args=()))
    for item in p17[::-1]:
        item.start()
    for item in p17:
        item.join(timeout = 90)
    for item in p17:
        item.terminate()
    print('-----------------------------------------------------------------------------------------------------------------------------------')


