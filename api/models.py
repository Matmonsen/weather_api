from django.db import models


class Forecast(models.Model):
    forecast_type = models.CharField(max_length=12)
    location = models.ForeignKey('Location')
    credit = models.ForeignKey('Credit')
    sun = models.ForeignKey('Sun')
    created = models.DateTimeField(auto_now_add=True)
    search = models.CharField(max_length=255)
    language = models.CharField(max_length=20)

    class Meta:
        get_latest_by = 'created'

    def to_dict(self):
        return dict(
            forecast_type=self.forecast_type,
            location=self.location.to_dict(),
            credit=self.credit.to_dict(),
            sun=self.sun.to_dict(),
            created=self.created,
            search=self.search,
            language=self.language)


class Time(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    period = models.IntegerField(null=True, blank=True)
    precipitation = models.ForeignKey('Precipitation')
    pressure = models.ForeignKey('Pressure')
    symbol = models.ForeignKey('Symbol')
    temperature = models.ForeignKey('Temperature')
    wind_direction = models.ForeignKey('WindDirection')
    wind_speed = models.ForeignKey('WindSpeed')
    forecast = models.ForeignKey('Forecast')

    class Meta:
        ordering = ['-start']

    def to_dict(self):
        return dict(
            start=self.start,
            end=self.end,
            period=self.period,
            precipitation=self.precipitation.to_dict(),
            pressure=self.pressure.to_dict(),
            symbol=self.symbol.to_dict(),
            temperature=self.temperature.to_dict(),
            wind_direction=self.wind_direction.to_dict(),
            wind_speed=self.wind_speed.to_dict()
        )


class Location(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    timezone = models.ForeignKey('TimeZone')

    def to_dict(self):
        return dict(
            name=self.name,
            type=self.type,
            country=self.country,
            timezone=self.timezone.to_dict()
        )


class TimeZone(models.Model):
    zone = models.CharField(max_length=255)
    utcoffsetMinutes = models.IntegerField()

    def to_dict(self):
        return dict(
            zone=self.zone,
            utcoffsetMinutes=self.utcoffsetMinutes
        )


class Credit(models.Model):
    url = models.URLField(max_length=255)
    text = models.CharField(max_length=255)

    def to_dict(self):
        return dict(
            url=self.url,
            text=self.text
        )


class Temperature(models.Model):
    unit = models.CharField(max_length=10)
    value = models.FloatField()

    def to_dict(self):
        return dict(
            unit=self.unit,
            value=self.value
        )


class Pressure(models.Model):
    unit = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=6, decimal_places=2, default=-1.0)

    def to_dict(self):
        return dict(
            unit=self.unit,
            value=self.value
        )


class WindDirection(models.Model):
    degree = models.DecimalField(max_digits=5, decimal_places=2, default=-1.0)
    name = models.CharField(max_length=245)
    code = models.CharField(max_length=10, blank=True, null=True)

    def to_dict(self):
        return dict(
            degree=self.degree,
            name=self.name,
            code=self.code
        )


class WindSpeed(models.Model):
    mps = models.DecimalField(max_digits=5, decimal_places=2, default=-1.0)
    name = models.CharField(max_length=245)

    def to_dict(self):
        return dict(
            mps=self.mps,
            name=self.name
        )


class Precipitation(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2, default=-1.0)
    min_value = models.DecimalField(max_digits=5, decimal_places=2, default=-1.0)
    max_value = models.DecimalField(max_digits=5, decimal_places=2, default=-1.0)

    def to_dict(self):
        return dict(
            value=self.value,
            min_value=self.min_value,
            max_value=self.max_value
        )


class Symbol(models.Model):
    name = models.CharField(max_length=245)
    number = models.IntegerField()
    var = models.CharField(max_length=10)

    def to_dict(self):
        return dict(
            name=self.name,
            number=self.number,
            var=self.var
        )


class Sun(models.Model):
    rise = models.DateTimeField()
    set = models.DateTimeField()

    def to_dict(self):
        return dict(
            rise=self.rise,
            set=self.set
        )
