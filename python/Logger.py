from time import ctime as t_ctime
from cfg import _LoggerFlag, get_logger_file, close_logger_file, WriteLogToFile


class Logger:
    """ A logger. """

    @property
    def version(self):
        return '1.0'

    @staticmethod
    def get_func_name(func):
        """
        Get a function's name. \n
        :param func: Current function.
        :return: (str)function's name if func is a function
                 else False(means it's not a function).
        """
        #            functions  class_method
        func_type = ['function', 'method']
        return func.__name__ if type(func).__name__ in func_type else False

    @staticmethod
    def will_log_to_file(msg: str) -> None:
        """ log msg to log file. """
        logger_file_fp = get_logger_file()
        print(msg, end='', file=logger_file_fp) if msg is not None else True
        close_logger_file(logger_file_fp)

    @staticmethod
    def will_log_to_stdout(msg: str) -> None:
        """ log msg to stdout. """
        print(msg, end='')

    @staticmethod
    def _log_a_string(string: str) -> None:
        Logger.will_log_to_file(string) if WriteLogToFile else Logger.will_log_to_stdout(string)

    @staticmethod
    def _log_an_exception(e):
        Logger._log_a_string(e.__name__)

    @staticmethod
    def _log_a_massage(massage: any) -> None:
        """ Log one massage according to its type. """
        name = Logger.get_func_name(massage)
        type_of_massage = type(massage).__name__
        type_of_name = type(name).__name__
        if type_of_name == 'str':
            Logger._log_a_string(f"[{name}]: ")
        elif type_of_massage == 'str':
            Logger._log_a_string(massage)
        elif type_of_massage == 'bool':
            pass
        elif type_of_massage == 'type':
            Logger._log_an_exception(massage)
        elif type_of_massage == 'property':
            Logger._log_a_string(f'(@p){massage}')

    @classmethod
    def log(cls, msg: list, c_func=False) -> None:
        """
        A logger. \n
        :param msg: A list consists of massages.
        :param c_func: Current function.
        :return: None
        """
        if _LoggerFlag:
            # Cast form 'Thu Jul 23 09:48:35 2020' to '09:48:35'
            now = f"[{' '.join(t_ctime().split(' ')[2:-1])}]"
            Logger._log_a_string(now)
            datas = [c_func] if c_func else []
            [datas.append(data) for data in msg]
            [Logger._log_a_massage(massage) for massage in datas]
            Logger.will_log_to_file('\n') if WriteLogToFile else Logger.will_log_to_stdout('\n')
