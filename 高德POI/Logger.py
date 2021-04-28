from queue import Queue
import threading,os,datetime,time,traceback


class Logger:
    def __init__(self, name):
        self.name = name
        self.queue = Queue()
        self.wth = threading.Thread(target=Logger.write_thread, args=(self,))
        self.wth.setDaemon(True)
        self.wth.start()

    def out(self, type, msg):
        msg = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')+"["+type+"]"+str(msg)
        print("["+self.name+"]"+msg)
        self.queue.put(msg)

    def info(self, msg):
        self.out("info", msg)

    def error(self, msg):
        self.out("error", msg)

    def debug(self, msg):
        self.out("debug", msg)

    def warn(self, msg):
        self.out("warn", msg)

    @staticmethod
    def write_thread(logger):
        path = os.path.dirname(__file__)+"/../logs"
        if not os.path.exists(path):
            os.mkdir(path)
        dt = datetime.datetime.now().strftime('%Y%m%d')
        fp = open(path + "/" + logger.name + "_" + dt + ".log", "a+")
        while 1:
            try:
                if not logger.queue.empty():
                    fp.write(logger.queue.get())
                    fp.write("\n")
                else:
                    fp.close()
                    dt = datetime.datetime.now().strftime('%Y%m%d')
                    fp = open(path + "/" + logger.name + "_" + dt + ".log", "a+")
                    time.sleep(1)
            except Exception as ex:
                fp.close()
                dt = datetime.datetime.now().strftime('%Y%m%d')
                fp = open(path + "/" + logger.name + "_" + dt + ".log", "a+")
                traceback.print_exc()


class LoggerFactory:
    LoggerPool = {}

    @staticmethod
    def getLogger(name):
        if name not in LoggerFactory.LoggerPool:
            LoggerFactory.LoggerPool[name] = Logger(name)
        return LoggerFactory.LoggerPool[name]