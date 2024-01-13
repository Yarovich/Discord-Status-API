import requests
import datetime
from typing import List


class _VoiceStatus:
    def __init__(self, components):
        self.Total: str = components[17]["status"]
        self.Brazil: str = components[2]["status"]
        self.Rotterdam: str = components[4]["status"]
        self.Hong_Kong: str = components[8]["status"]
        self.India: str = components[13]["status"]
        self.Japan: str = components[15]["status"]
        self.Russia: str = components[18]["status"]
        self.Singapore: str = components[19]["status"]
        self.South_Africa: str = components[21]["status"]
        self.South_Korea: str = components[23]["status"]
        self.Sydney: str = components[25]["status"]
        self.US_Central: str = components[27]["status"]
        self.US_East: str = components[28]["status"]
        self.US_South: str = components[29]["status"]
        self.US_West: str = components[30]["status"]


class _ClientStatus:
    def __init__(self, components):
        self.Total: str = components[20]["status"]
        self.Desktop: str = components[3]["status"]
        self.iOS: str = components[7]["status"]
        self.Android: str = components[11]["status"]
        self.Web: str = components[14]["status"]


class _ThirdPartyStatus:
    def __init__(self, components):
        self.Total: str = components[22]["status"]
        self.CloudFlare: str = components[1]["status"]
        self.Tax_Calculation_Service: str = components[6]["status"]
        self.Creator_Payouts: str = components[9]["status"]


class _DataInfo:
    def __init__(self, data: dict):
        self.timestamp: datetime.datetime = datetime.datetime.utcfromtimestamp(data["timestamp"])
        self.value: int = data['value']


class _SM_Status:
    def __init__(self, current: str):
        response = requests.get(f"https://discordstatus.com/metrics-display/5k2rt9f7pmny/{current}.json").json()
        self.last_fetched_at: str = response["metrics"][0]["metric"]["last_fetched_at"]
        self.sum: float = response["summary"]["sum"]
        self.mean: float = response["summary"]["mean"]
        self.last: int = response["summary"]["last"]
        data = []
        for i in response["metrics"][0]["data"]:
            data.append(_DataInfo(i))
        self.data: List[_DataInfo] = data


class _SystemMetricsStatus:
    @property
    def Day(self) -> _SM_Status:
        return _SM_Status("day")

    @property
    def Week(self) -> _SM_Status:
        return _SM_Status("week")

    @property
    def Month(self) -> _SM_Status:
        return _SM_Status("month")


class _Incident:
    def __init__(self, info: dict):
        self.name: str = info["name"]
        self.status: str = info["status"]
        self.created_at: str = info["created_at"]
        self.updated_at: str = info["updated_at"]
        self.monitoring_at: str = info["monitoring_at"]
        self.resolved_at: str = info["resolved_at"]
        self.impact: str = info["impact"]
        self.shortlink: str = info["shortlink"]


def get_all_incidents() -> List[_Incident]:
    response = requests.get("https://discordstatus.com/api/v2/incidents.json").json()
    incidents = []
    for info in response["incidents"]:
        incidents.append(_Incident(info))
    return incidents


def get_all_unresolved_incidents() -> List[_Incident]:
    response = requests.get("https://discordstatus.com/api/v2/incidents/unresolved.json").json()
    incidents = []
    for info in response["incidents"]:
        incidents.append(_Incident(info))
    return incidents


class Status:
    def __init__(self):
        response = requests.get("https://discordstatus.com/api/v2/summary.json").json()
        components = response["components"]
        self.description = response["status"]["description"]
        self.indicator = response["status"]["indicator"]
        self.API: str = components[0]["status"]
        self.MediaProxy: str = components[5]["status"]
        self.Gateway: str = components[10]["status"]
        self.PushNotifications: str = components[12]["status"]
        self.Search: str = components[16]["status"]
        self.Voice: _VoiceStatus = _VoiceStatus(components)
        self.Client: _ClientStatus = _ClientStatus(components)
        self.Third_party: _ThirdPartyStatus = _ThirdPartyStatus(components)
        self.Server_Web_Pages: str = components[24]["status"]
        self.Payments: str = components[26]["status"]

    @property
    def All_Incidents(self) -> List[_Incident]:
        return get_all_incidents()

    @property
    def Unresolved_Incidents(self) -> List[_Incident]:
        return get_all_unresolved_incidents()

    @property
    def System_Metrics(self) -> _SystemMetricsStatus:
        return _SystemMetricsStatus()
