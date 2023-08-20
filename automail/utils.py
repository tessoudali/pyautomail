import logging
import configparser
import coloredlogs


def init_logger(name='', filename=None, level=logging.CRITICAL):
    """This function will initialize a logger object

    Parameters
    ----------
    name : str
        The name of the logger object. If not specified, the name will be the root logger.
    filename : str
        The path where the log file is created. If it isn't set, no log file is created.
    level : int
        the level of logger

    Returns
    -------
    logger_obj : logging.Logger
        The logger object.

    Notes
    -----
    This function will initialize a logger object with the following format::

        [%(asctime)s - %(levelname)s (%(name)s) ] : %(message)s


    Example
    -------
    The logger object will log to both stdout and a file.
    After colling this function you can use logger_obj to log.

    >>> logger_obj = init_logger('EmailSender')
    >>> logger_obj.debug('debug message')
    [2019-08-20 15:30:00,000 - DEBUG (EmailSender) ] : debug message
    >>> logger_obj.info('info message')
    [2019-08-20 15:30:00,000 - INFO (EmailSender) ] : info message
    >>> logger_obj.warning('warning message')
    [2019-08-20 15:30:00,000 - WARNING (EmailSender) ] : warning message
    >>> logger_obj.error('error message')
    [2019-08-20 15:30:00,000 - ERROR (EmailSender) ] : error message
    >>> logger_obj.critical('critical message')
    [2019-08-20 15:30:00,000 - CRITICAL (EmailSender) ] : critical message


    """
    logger_obj = logging.getLogger(name)
    coloredlogs.install(logger=logger_obj, fmt='[%(asctime)s - %(levelname)s (%(name)s) ] : %(message)s')
    logger_obj.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s - %(levelname)s (%(name)s) ] : %(message)s')
    if filename is not None:
        handler2 = logging.FileHandler(filename)
        handler2.setFormatter(formatter)
        logger_obj.addHandler(handler2)
    return logger_obj


def create_config_file(smtp_server, smtp_port, sender_email='', password='', is_test=False):
    """This function will create a config file for the email sender.

    Parameters
    ----------
    smtp_server : str
        The SMTP server address.
    smtp_port : int
        The SMTP server port.
    sender_email : str
        The email address of the sender.
    password : str
        The password of the sender.
    is_test : bool
        If True, the email will not be sent.

    Notes
    -----
    This function will create a config file with the following format::

        [SMTP]
        server = smtp.gmail.com
        port = 465

        [SENDER]
        email = example@gmail.com
        password = password

    """
    with open('./config.cfg', 'w') as f:
        f.write('[smtp]\n')
        f.write(f'host = {smtp_server}\n')
        f.write(f'port = {smtp_port}\n')
        f.write(f'is_test = {is_test}\n')
        f.write('\n')
        f.write('[account]\n')
        f.write(f'user = {sender_email}\n')
        f.write(f'password = {password}\n')


def read_config_file():
    """This function will read the config file.

    Returns
    -------
    config : configparser.ConfigParser
        The config object.

    Notes
    -----
    This function will read the config file with the following format::

        [SMTP]
        server = smtp.gmail.com
        port = 465

        [SENDER]
        email = exxample@gmail.com
        password = password

    """
    config = configparser.ConfigParser()
    config.read('./config.cfg')
    return config


def get_config_dict():
    """This function will get the email sender config.

    Returns
    -------
    config : configparser.ConfigParser
        The config object.

    Notes
    -----
    This function will read the config file with the following format::

        [SMTP]
        server = smtp.gmail.com
        port = 465

        [SENDER]
        email =
        password =

    """
    config = read_config_file()
    config_dict = {
        'smtp_server': config.get('smtp', 'server', fallback=''),
        'smtp_port': config.getint('smtp', 'port', fallback=0),
        'is_test': config.getboolean('smtp', 'is_test', fallback=False),
        'user': config.get('account', 'user', fallback=''),
        'password': config.get('account', 'password', fallback='')
    }
    return config_dict