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
        if (len(day) == 3) and (day.upper() in self.__start_times.keys()):
            open = self.__start_times[day]
            close = self.__end_times[day]
            return open, close
        else:
            return ValueError

    @property
    def get_timings(self):
        return self.__start_times, self.__end_times