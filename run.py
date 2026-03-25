import multiprocessing

# Start Jarvis
def startJarvis():
    print("Jarvis is starting...")
    from main import start
    start()

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=startJarvis)
    p1.start()
    p1.join()

    print("System stopped")