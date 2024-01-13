from DiscordStatusAPI import Status

status = Status()

print(status.description)

print(f"Voice status: {status.Voice.Russia}")

sys_mtrcs = status.System_Metrics.Day
print(f"API Response Time: {sys_mtrcs.last}")

unres_inc = status.Unresolved_Incidents
if len(unres_inc) != 0:
    inc = unres_inc[0]
    print(f"Unresolved Incidents: {inc.name} - {inc.status} - {inc.impact}")
else:
    print("Unresolved Incidents: None")
