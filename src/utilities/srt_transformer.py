import srt


class SrtTransformer:

    def __init__(self, file, function):
        self.file = file
        self.function = function
        self.srt_list = self._read_from_file()

    def transform(self, *args):
        self.srt_list = self.function(self.srt_list, *args)
        self.srt_list = list(srt.sort_and_reindex(self.srt_list))

    def write_to_file(self, file=None):
        if self.srt_list is None:
            print('Skipping {} because of bad srt format.'.format(self.file))
            return
        if file is None:
            file = self.file
        with open(file, "w", encoding="utf-8") as f:
            f.write(srt.compose(self.srt_list))

    def _read_from_file(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(self.file, "r") as f:
                content = f.read()
        try:
            return list(srt.parse(content))
        except:
            return None



