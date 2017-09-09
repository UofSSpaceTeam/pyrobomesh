# File ProcessManager.py
# 
# THIS FILE IS SUBJECT TO THE LICENSE TERMS GRANTED BY THE UNIVERSITY OF SASKATCHEWAN SPACE TEAM (USST).

from threading import Thread # Threads are fully functional on Windows.
from multiprocessing.context import Process # Processes are fully functional on Windows.
import time
import sys
from subprocess import Popen

class RoboProcesses:
    def __init__(self, cmd):
        self.cmd = cmd
        self.popen = None
    def execute(self):
        self.popen = Popen(self.cmd)



class ProcessManager:
    """
    Class: ProcessManager

    This class represents the pocessing module for the robocluster operating system.
    """


    def __init__(self, **kwargs):
        """Initializes the process manager"""
        self.process_dict = {} # Process dictionary: stores all processes
        return super().__init__(**kwargs)

    def isEmpty(self):
        """
        Confirms whether process_dict is empty.
        """
        if self.process_dict == {}:
            return True
        else:
            return False

    def createProcess(self, name, command):
        """
        Creates a process.
        Checks if command is type string if so it returns True otherwise it returns False.
        Checks if name has not been used otherwise informs that name is taken.

        """
        if type(command) == str:
            if name in self.process_dict:
                print("Name already taken.")
            else:
                self.process_dict[name] = RoboProcesses(command)
            return True
        else:
            return False





    def createThread(self):
        """
        TODO create a function that takes in parameters and uses those parameters to
        ceate one single thread. The thread must then be stored in "self.T".
        """

    def startProcess(self, name):
        """
        Starts a single process.
        """
        self.process_dict[name].execute()


    def startAllProcesses(self):
        """
        Starts all processes in process_dict.
        """

        for process in self.process_dict:
            self.startProcess(process)

    def stopProcess(self, name):
        """
        Stops a specific process in process_dict.
        """

        print ("Shutting down " + name)
        self.process_dict[name].popen.kill()
        self.process_dict[name].popen.wait()


    def stopAllProcesses(self):
        """
        Stops all processes in process_dict.
        """

        print ("Shutting down")

        for process in self.process_dict:
            self.process_dict[process].popen.kill()
            self.process_dict[process].popen.wait()

    def status(self, thread):
        if self.isEmpty():
            return None
        else:
            None
        """
        TODO: Return the status of a thread or process
        """

    def verify(self, thread):
        """
        TODO: Check the status of the thread or process and perform certain functions based on its status.
        """

    def fix(self, thread):
        """
        TODO: Fix a thread or process if its not running properly. 
        """

threadNames = [] # This list is currently used for testing purposes.
# Once the threading module is working fine, then we can begin connecting the proceses through 0mq.
if __name__ == "__main__":
    taskMgr=ProcessManager()
    for name in threadNames: # Create threads for each rover software
        taskMgr.createThread(name)

    taskMgr.startAllProcesses()

    try:
        while True: # Execute the processes.
            """
            TODO Run the processes as they should.
            """
            for task in taskMgr.T: # Verify tasks.
                taskMgr.verify(task.name)
            time.sleep(3)
    except KeyboardInterrupt:
        taskMgr.stopAllProcesses()
        sys.exit(0)