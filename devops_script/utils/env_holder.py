
class EnvHolder:

    evn_dict = {}

    @classmethod
    def put(self, key, value):
        self.evn_dict[key] = value

    @classmethod
    def get(self, key):
        return self.evn_dict[key]