from multiprocessing import Process
from touchless_mouse import touchless_mouse

if __name__ == "__main__":
    touchless_process = Process(target=touchless_mouse)
    touchless_process.start()
    touchless_process.join()
