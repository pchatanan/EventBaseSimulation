NUM_CHANNELS = 10


class Station:
    # station properties
    busy_channel_count = None

    def __init__(self):
        self.busy_channel_count = 0

    def get_available_channel(self):
        return NUM_CHANNELS - self.busy_channel_count
