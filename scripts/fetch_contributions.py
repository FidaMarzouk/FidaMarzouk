"""Pulls Fida's contribution calendar (one entry per calendar year) and public repo count
from the GitHub GraphQL API into data/contributions.json. Needs GH_TOKEN (a token for this account)."""
import datetime as dt, json, os, urllib.request

LOGIN = "FidaMarzouk"
TOKEN = os.environ["GH_TOKEN"]
Q = """query($login:String!,$from:DateTime!,$to:DateTime!){
  user(login:$login){
    createdAt
    repositories(privacy:PUBLIC, isFork:false){ totalCount }
    contributionsCollection(from:$from,to:$to){
      contributionCalendar{ weeks{ contributionDays{ date contributionCount } } }
    }
  }
}"""


def gql(variables):
    req = urllib.request.Request("https://api.github.com/graphql",
                                 data=json.dumps({"query": Q, "variables": variables}).encode(),
                                 headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"})
    out = json.load(urllib.request.urlopen(req))
    if "errors" in out:
        raise SystemExit(out["errors"])
    return out["data"]["user"]


today = dt.date.today()
first = gql({"login": LOGIN, "from": f"{today.year}-01-01T00:00:00Z", "to": f"{today.isoformat()}T23:59:59Z"})
start_year = max(int(first["createdAt"][:4]), today.year - 2)  # the three most recent years, like GitHub's tabs
years = {}
for y in range(start_year, today.year + 1):
    u = first if y == today.year else gql({"login": LOGIN, "from": f"{y}-01-01T00:00:00Z", "to": f"{y}-12-31T23:59:59Z"})
    days = {d["date"]: d["contributionCount"]
            for w in u["contributionsCollection"]["contributionCalendar"]["weeks"]
            for d in w["contributionDays"] if d["contributionCount"] and d["date"].startswith(str(y))}
    years[str(y)] = days

os.makedirs("data", exist_ok=True)
json.dump({"updated": today.isoformat(), "public_repos": first["repositories"]["totalCount"], "years": years},
          open("data/contributions.json", "w"), indent=1)
print({y: sum(d.values()) for y, d in years.items()})
