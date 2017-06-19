"""
Utility method to format the container stats retrieved
from docker API
"""


def bytes_to_human(_bytes):
    """
    Format given bytes as KB or MB
    :param _bytes: Number to format
    :return: Formatted string representation of given bytes
    """

    if bytes_to_mb(_bytes) < 1:
        return '{} KB'.format(round(bytes_to_kb(_bytes), 2))
    else:
        return '{} MB'.format(round(bytes_to_mb(_bytes), 2))


def bytes_to_kb(_bytes):
    return float(_bytes) / 1024


def bytes_to_mb(_bytes):
    return bytes_to_kb(_bytes) / 1024


def calculate_cpu_percent(previous_cpu, previous_system, cpu_usage,
                          system_usage, cores):
    """ Calculates the container CPU usage percent
    Based on official client algorithm: https://goo.gl/3QKoNv

    Execs calculations using cpu usage in between readings
    :param previous_cpu: Container CPU usage from previous reading
    :param previous_system: System CPU usage from previous reading
    :param cpu_usage: Container CPU usage
    :param system_usage: System CPU usage
    :param cores: Number of active cores
    :return:
    """
    cpu_percent = 0

    # CPU Container usage change in between readings
    cpu_delta = cpu_usage - previous_cpu

    # CPU System usage change in between readings
    system_delta = system_usage - previous_system

    if system_delta > 0 and cpu_delta > 0:
        cpu_percent = (float(cpu_delta) / system_delta) * cores * 100
        cpu_percent = round(cpu_percent, 2)

    return cpu_percent


def calculate_mem_percent(memory_usage, memory_limit):
    """
    Calculates the amount percent of used memory by a container

    :param memory_usage: Container memory usage
    :param memory_limit: Max allowed memory
    :return:
    """
    mem_percent = 0

    if memory_limit > 0 and memory_usage > 0:
        mem_percent = (float(memory_usage) / memory_limit) * 100
        mem_percent = round(mem_percent, 2)

    return mem_percent
