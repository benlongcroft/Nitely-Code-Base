class timings:
    """timings object can hold opening time and closing time for venue"""

    def __init__(self, start_times, end_times):
        self.__start_times = start_times
        self.__end_times = end_times

    def get_day(self, day):
        """
        Gets opening and closing times for a specific day
        :param day: string in format MON, TUE, WED, THU, FRI, SAT or SUN
        :return: opening time and closing time as string
        """
        open_t = self.__start_times[day]
        close_t = self.__end_times[day]
        return open_t, close_t

    @property
    def get_timings(self):
        return self.__start_times, self.__end_times

    def __repr__(self):
        return str([[self.__start_times[i], self.__end_times[i]] for i in self.__start_times.keys()])
