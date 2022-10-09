from pydantic import BaseModel, confloat, Field, constr
from typing import Literal


DateTimeISO8601 = str
Status = Literal["AVAILABLE", "CHARGING", "OUTOFORDER", "UNKNOWN"]
EvseId = constr(regex=r"^([A-Z]+)\*([A-Z0-9]+)\*([A-Z0-9]*)(?:\*([A-Z0-9]+))?$")


class Coordinates(BaseModel):
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)


class Connector(BaseModel):
    id: int
    status: Status
    standard: Literal["IEC_62196_T2", "IEC_62196_T2_COMBO", "DOMESTIC_F", "CHADEMO", "TESLA"]
    format: Literal["CABLE", "SOCKET"]
    power_type: Literal["AC_1_PHASE", "AC_3_PHASE", "DC"]
    ampere: float
    voltage: float
    max_power: float
    tariff_id: str | None


class Evse(BaseModel):
    uid: str
    id: EvseId
    status: Status
    reservable: bool
    capabilities: list[str]
    physical_reference: str | None
    floor_level: str | None
    vehicle_type: str
    charge_point_position: str = Field(..., alias="chargePointPosition")
    charge_point_public_comment: str | None = Field(
        ..., alias="chargePointPublicComment"
    )
    charge_point_parking_space_numbers: str | None = Field(
        ..., alias="chargePointParkingSpaceNumbers"
    )
    charging_station_position: str | None = Field(..., alias="chargingStationPosition")
    roaming: bool
    connectors: list[Connector]


class Operator(BaseModel):
    operator_id: str = Field(..., alias="operatorId")
    name: str
    hotline: str


class OpeningTimes(BaseModel):
    twentyfourseven: bool


class Location(BaseModel):
    id: int
    name: str
    status: str
    address: str
    city: str
    postal_code: str
    country: str
    directions: str | None
    coordinates: Coordinates
    distance_in_m: str
    operator: Operator
    opening_times: OpeningTimes
    owner: str | None
    roaming: bool
    evses: list[Evse]
    tariff_zones: list[str] = Field(..., alias="tariffZones")


class Response(BaseModel):
    data: list[Location]
    status_code: str
    status_message: str
    timestamp: DateTimeISO8601
