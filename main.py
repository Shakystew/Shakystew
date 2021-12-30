"""-------------
@Shakystew
-------------"""

from skyfield.api import load, EarthSatellite, wgs84


class sattract(object):
    """
    Description: TBD
    """

    def __init__(self, filename, lat, lon, alt):
        """
        :param filename: {str} /full/path/to/TLE file
        :param lat:  {float} degrees, current location latitude
        :param lon:  {float} degrees, current location longitude
        :param alt:  {float} degrees, current location altitude
        """
        self.filename = filename

        self.bluffton = wgs84.latlon(lat, lon, alt)  # Instantiating current location
        self.ts = load.timescale()  # Instantiating relative timescale

    def tle(self):
        """
        Description: Instantiating EarthSatellite <objects> from TLE file
        :return: {list} EarthSatellite <objects>
        """
        with open(self.filename, "r") as f:

            lines = f.readlines()
            self.satellites = []

            # Checking TLE format, 3LE
            if lines[0].split()[0] == "0":
                for t0, t1, t2 in zip(lines[0::2], lines[1::2], lines[2::2]):
                    self.satellites.append(EarthSatellite(t1, t2, t0, self.ts))
            # Checking TLE format, conventional two-row TLE
            elif lines[0].split()[0] == "1":
                for t1, t2 in zip(lines[1::2], lines[2::2]):
                    self.satellites.append(EarthSatellite(t1, t2, "", self.ts))
            else:
                print("Error:\tTLE file (%s) is not 3LE format." % self.filename)
                print("Error:\tFailed to load TLE file (%s).")
        return

    def inview(self, satellite, start, end, above=30.0):
        """
        Description: Calculates time windows when satellite is in view
        :param satellite: {object} EarthSatellite <object> to query
        :param start:   {datetime} start of time to query <inview>
        :param end:     {datetime} end of time to query <inview>
        :param above:   {float} degree above horizon to track satellite
        :return: {list} rise, peak, set of datetimes
        """
        times, events = satellite.find_events(
            self.bluffton, start, end, altitude_degrees=above
        )
        rise = [x.utc_datetime() for x in times[0::3]]
        peak = [x.utc_datetime() for x in times[1::3]]
        set = [x.utc_datetime() for x in times[2::3]]
        return rise, peak, set

    def main(self):
        self.tle()
        return self.inview(
            self.satellites[30000], self.ts.utc(2021, 12, 1), self.ts.utc(2021, 12, 31)
        )


if __name__ == "__main__":
    tle_file = "./tle_sample.tle"
    lat = 38.804410
    lon = -77.051930
    alt = 0
    rise, peak, set = sattract(filename=tle_file, lat=lat, lon=lon, alt=alt).main()
