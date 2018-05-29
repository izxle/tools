from .result import Result


class Report:
    def __init__(self):
        pass


class ReportSingle(Report):
    def __init__(self, result):
        super().__init__()
        self.result = result

    def __str__(self):
        r = self.result
        text = (
            f'{r.name}\n'
            f'{r.oszicar}'
            f'time: {r.time/3600:8.4f} h | {r.time:9.3f} s')
        return text


class ReportCompare(Report):
    def __init__(self):
        super.__init__()


class ReportAdsorption(Report):
    def __init__(self):
        super.__init__()


class ReportSurface(Report):
    def __init__(self):
        super.__init__()

