import multiprocessing

def startAssistant():
    # Process 1 Code
    print("Process 1 is running.")
    from main import start
    start()


def listenHotword():
    # Process 2 Code
    print("Process 2 is running.")
    from engine.features import hotword
    hotword()


if __name__ == '__main__':
    proc1 = multiprocessing.Process(target=startAssistant)
    proc2 = multiprocessing.Process(target=listenHotword)
    proc1.start()
    proc2.start()
    proc1.join()

    if proc2.is_alive():
        proc2.terminate()
        proc2.join()

    print("System stop")
