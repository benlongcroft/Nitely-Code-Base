class timings:
    def __init__(self, start_times, end_times):
        self.__start_times = start_times
        self.__end_times = end_times

    def get_day(self, day):
        if (len(day) == 3) and (day.upper() in self.__start_times.keys()):
            open = self.__start_times[day]
            close = self.__end_times[day]
            return open, close
        else:
            return ValueError

    def get_timings(self):
        return self.__start_times, self.__end_times