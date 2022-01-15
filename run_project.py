from multiprocessing import Process
import subprocess
import os


def runBackendProcess():
    # run the script for initializing DB and start Main Server and telegram server
    print("----------Running Backend...------------")
    #os.system("python main.py")
    #subprocess.check_call('python -m flask run', shell=True)
    subprocess.check_call('python main.py', shell=True)


def runFrontedProcess():
    print("----------Running Fronted...------------")
    #os.system("cd fronted_react")
    os.chdir("./fronted_react")
    subprocess.check_call('npm install', shell=True) # I guess this should come first
    subprocess.check_call('npm start', shell=True)



# This is a sample Python script.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # os.system('conda env create -f environment.yml') # creating the conda env, from conda prompt
    # backend_process
    backend_process = Process(target=runBackendProcess)
    backend_process.start()
    # backend_process.join()

    # fronted process
    fronted_process = Process(target=runFrontedProcess)
    fronted_process.start()
    # fronted_process.join()


