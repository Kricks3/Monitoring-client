import json
import platform
import re
from subprocess import PIPE, run


class MachineStats(object):
    def __init__(self):
        self.machine = platform.machine()
        self.processor = platform.processor()
        self.system = platform.system()
        self.version = platform.version()
        self.programs = self._get_all_programs()

    def _get_all_programs(self):
        command = 'wmic product get name,version'
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        programs = self._parse_wmic_output(result.stdout)
        return programs

    @staticmethod
    def _parse_wmic_output(text):
        result = []
        # remove empty lines
        lines = [s for s in text.splitlines() if s.strip()]

        if not lines:
            return result
        header_line = lines[0]

        # Find headers and their positions
        headers = re.findall('\\S+\\s+|\\S$', header_line)
        pos = [0]
        for header in headers:
            pos.append(pos[-1] + len(header))

        # Delete all spaces in header
        for i in range(len(headers)):
            headers[i] = headers[i].strip()

        # Parse each entries
        for r in range(1, len(lines)):
            row = {}
            for i in range(len(pos) - 1):
                row[headers[i]] = lines[r][pos[i]:pos[i + 1]].strip()
            result.append(row)
        return result


class MachineStatsEncoder(json.JSONEncoder):
    def default(self, o):# pylint: disable=E0202
        if isinstance(o, MachineStats):
            return o.__dict__
        return json.JSONEncoder.default(self, o)


# Только для проверки, потом убери это
# src = MachineStats()
# data = json.dumps(src, cls=MachineStatsEncoder)
# print(data)
