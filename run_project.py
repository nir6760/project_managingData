from multiprocessing import Process
import os


def runBackendProcess():
    # run the script for initializing DB and start Main Server and telegram server
    print('Run Backend:')
    os.system("python main.py")


def runFrontedProcess():
    print('Run Fronted:')
    os.system("cd fronted_react")
    os.system("npm install")  # I guess this should come first
    os.system("npm start")


# This is a sample Python script.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.system()
    # backend_process
    backend_process = Process(target=runBackendProcess)
    backend_process.start()
    # backend_process.join()

    # fronted process
    fronted_process = Process(target=runFrontedProcess)
    fronted_process.start()
    # fronted_process.join()
