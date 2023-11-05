from bcdd import data, bc_csv
from typing import Optional, Union


class ServerDataSegment:
    def __init__(
        self,
        filter_date_enabled: int,
        filter_start_datemmdd: Optional[int],
        filter_start_datehhmm: Optional[str],
        filter_end_date_mmdd: Optional[int],
        filter_end_date_hhmm: Optional[str],
        filter_day_flags: list[bool],
        filter_week_flag: int,
        filter_start_times: list[str],
        filter_end_times: list[str],
    ):
        self.filter_date_enabled = filter_date_enabled
        self.filter_start_datemmdd = filter_start_datemmdd
        self.filter_start_datehhmm = filter_start_datehhmm
        self.filter_end_date_mmdd = filter_end_date_mmdd
        self.filter_end_date_hhmm = filter_end_date_hhmm
        self.filter_day_flags = filter_day_flags
        self.filter_week_flag = filter_week_flag
        self.filter_start_times = filter_start_times
        self.filter_end_times = filter_end_times

    @staticmethod
    def from_line(
        line: "bc_csv.Row", start_index: int
    ) -> tuple["ServerDataSegment", int]:
        filter_date_enabled = line[0 + start_index].to_int()
        filter_start_datemmdd = None
        filter_start_datehhmm = None
        filter_end_date_mmdd = None
        filter_end_date_hhmm = None
        if filter_date_enabled:
            mmdd = line[1 + start_index].to_int()
            hhmm = line[2 + start_index].to_str()
            filter_start_datemmdd = mmdd
            filter_start_datehhmm = hhmm

            mmdd = line[3 + start_index].to_int()
            hhmm = line[4 + start_index].to_str()
            start_index += 4
            filter_end_date_mmdd = mmdd
            filter_end_date_hhmm = hhmm

        filter_day_count = line[1 + start_index].to_int()
        filter_day_flags: list[bool] = [False] * 31
        for i in range(filter_day_count):
            filter_day_flags[line[2 + start_index].to_int() - 1] = True
            start_index += 1

        filter_week_flag = line[2 + start_index].to_int()
        filter_time_count = line[3 + start_index].to_int()

        filter_start_times: list[str] = []
        filter_end_times: list[str] = []

        for i in range(filter_time_count):
            hhmm = line[4 + start_index + (i * 2)].to_str()
            filter_start_times.append(hhmm)

            hhmm = line[5 + start_index + (i * 2)].to_str()
            filter_end_times.append(hhmm)

        server_data_segment = ServerDataSegment(
            filter_date_enabled,
            filter_start_datemmdd,
            filter_start_datehhmm,
            filter_end_date_mmdd,
            filter_end_date_hhmm,
            filter_day_flags,
            filter_week_flag,
            filter_start_times,
            filter_end_times,
        )

        return server_data_segment, 5 + start_index + ((filter_time_count - 1) * 2)

    def serialize(self) -> list[Union[int, str]]:
        line: list[Union[int, str]] = []
        line.append(int(self.filter_date_enabled))
        if self.filter_date_enabled:
            line.append(self.filter_start_datemmdd or 0)
            line.append(self.filter_start_datehhmm or "")
            line.append(self.filter_end_date_mmdd or 0)
            line.append(self.filter_end_date_hhmm or "")

        line.append(sum(self.filter_day_flags))
        for i, flag in enumerate(self.filter_day_flags):
            if flag:
                line.append(i + 1)

        line.append(self.filter_week_flag)
        line.append(len(self.filter_start_times))
        for i in range(len(self.filter_start_times)):
            line.append(self.filter_start_times[i])
            line.append(self.filter_end_times[i])

        return line


class ServerData:
    def __init__(
        self,
        start_timeyyyymmdd: int,
        start_timehhmm: str,
        end_timeyyyymmdd: int,
        end_timehhmm: str,
        min_game_version: int,
        max_game_version: int,
        platform_flag: int,
        segments: list[ServerDataSegment],
    ):
        self.start_timeyyyymmdd = start_timeyyyymmdd
        self.start_timehhmm = start_timehhmm
        self.end_timeyyyymmdd = end_timeyyyymmdd
        self.end_timehhmm = end_timehhmm
        self.min_game_version = min_game_version
        self.max_game_version = max_game_version
        self.platform_flag = platform_flag
        self.segments = segments

    @staticmethod
    def from_line(line: "bc_csv.Row") -> tuple["ServerData", int]:
        yyyymmdd = line[0].to_int()
        hhmm = line[1].to_str()
        start_timeyyyymmdd = yyyymmdd
        start_timehhmm = hhmm

        yyyymmdd = line[2].to_int()
        hhmm = line[3].to_str()
        end_timeyyyymmdd = yyyymmdd
        end_timehhmm = hhmm

        min_game_version = line[4].to_int()
        max_game_version = line[5].to_int()
        platform_flag = line[6].to_int()

        length = line[7].to_int()
        segments: list[ServerDataSegment] = []
        index = 7
        for _ in range(length):
            segment, index = ServerDataSegment.from_line(line, index + 1)
            segments.append(segment)
        server_data = ServerData(
            start_timeyyyymmdd,
            start_timehhmm,
            end_timeyyyymmdd,
            end_timehhmm,
            min_game_version,
            max_game_version,
            platform_flag,
            segments,
        )
        return server_data, index

    def serialize(self) -> list[Union[int, str]]:
        line: list[Union[int, str]] = []
        line.append(self.start_timeyyyymmdd)
        line.append(self.start_timehhmm)
        line.append(self.end_timeyyyymmdd)
        line.append(self.end_timehhmm)
        line.append(self.min_game_version)
        line.append(self.max_game_version)
        line.append(self.platform_flag)
        line.append(len(self.segments))
        for segment in self.segments:
            line.extend(segment.serialize())
        return line


class SaleData:
    def __init__(self, dt: "data.Data"):
        self.server_data: list[ServerData] = []
        self.targets: list[list[int]] = []
        self.unknowns: list[tuple[int, int]] = []
        self.csv = bc_csv.CSV(dt, "\t")
        self.parse()

    def parse(self):
        for j, line in enumerate(self.csv):
            if line[0].to_str() == "[start]" or line[0].to_str() == "[end]":
                continue
            server_data, index = ServerData.from_line(line)
            total_targets = line[index + 1].to_int()
            targets: list[int] = []
            for i in range(total_targets):
                target = line[index + 2 + i].to_int()
                targets.append(target)

            if (index + 2 + total_targets) < len(line):
                self.unknowns.append((j - 1, line[index + 2 + total_targets].to_int()))
            self.targets.append(targets)
            self.server_data.append(server_data)

    def serialize(self) -> "data.Data":
        csv = bc_csv.CSV(data.Data(), "\t")
        csv.add_line(["[start]"])
        for i, server_data in enumerate(self.server_data):
            line = server_data.serialize()
            line.append(len(self.targets[i]))
            for target in self.targets[i]:
                line.append(target)
            for unknown in self.unknowns:
                if unknown[0] == i:
                    line.append(unknown[1])

            csv.add_line(line)
        csv.add_line(["[end]"])
        return csv.to_data()

    def get_server_data(self, index: int) -> ServerData:
        return self.server_data[index]

    def get_targets(self, index: int) -> list[int]:
        return self.targets[index]
