"""One parser per Orbisa system. Each turns raw export files into Graphiti episodes."""

import csv
import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup
from graphiti_core.nodes import EpisodeType
from pypdf import PdfReader

from context.config import DATA_DIR


@dataclass
class Episode:
    name: str
    system: str
    body: str
    source: EpisodeType
    reference_time: datetime
    description: str
    path: str = field(default="")

    @property
    def digest(self) -> str:
        return hashlib.sha256(self.body.encode()).hexdigest()[:16]


def _rel(path: Path) -> str:
    return path.relative_to(DATA_DIR).as_posix()


def _utc(value: str, fmt: str) -> datetime:
    return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)


def _iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _table_text(soup: BeautifulSoup) -> None:
    for table in soup.find_all("table"):
        rows = [" | ".join(c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])) for tr in table.find_all("tr")]
        table.replace_with("\n".join(rows) + "\n")


def confluence() -> list[Episode]:
    episodes = []
    for path in sorted((DATA_DIR / "confluence").glob("*_*.html")):
        soup = BeautifulSoup(path.read_text(), "html.parser")
        title = soup.select_one("#title-text").get_text(strip=True).removeprefix("Orbisa Wiki :").strip()
        meta = soup.select_one(".page-metadata").get_text(" ", strip=True)
        modified = _utc(re.search(r"on (\w{3} \d{2}, \d{4})", meta).group(1), "%b %d, %Y")
        content = soup.select_one("#main-content")
        _table_text(content)
        text = re.sub(r"\n{3,}", "\n\n", content.get_text("\n", strip=True))
        body = f"Confluence page: {title}\n{meta}\n\n{text}"
        episodes.append(Episode(_rel(path), "confluence", body, EpisodeType.text, modified,
                                f"Confluence (Orbisa wiki) page '{title}'", _rel(path)))
    return episodes


def _notion_edited(text: str) -> datetime:
    raw = re.search(r"Last edited time: (.+)", text).group(1).strip()
    return _utc(raw, "%B %d, %Y %I:%M %p")


def notion() -> list[Episode]:
    episodes = []
    root = DATA_DIR / "notion"
    for path in sorted(root.rglob("*.md")):
        text = path.read_text()
        title = text.splitlines()[0].lstrip("# ").strip()
        body = f"Brisklane Notion handbook page (read-only since the Orbisa acquisition): {title}\n\n{text}"
        episodes.append(Episode(_rel(path), "notion", body, EpisodeType.text, _notion_edited(text),
                                f"Notion (Brisklane handbook) page '{title}'", _rel(path)))
    for path in sorted(root.rglob("*.csv")):
        with path.open(newline="") as fh:
            for i, row in enumerate(csv.DictReader(fh), start=1):
                edited = _utc(row["Last edited time"], "%B %d, %Y %I:%M %p")
                payload = {"source": "Brisklane Notion customer list (read-only)", **row}
                episodes.append(Episode(f"{_rel(path)}#row{i}", "notion", json.dumps(payload), EpisodeType.json, edited,
                                        "Notion (Brisklane handbook) customer database row", _rel(path)))
    return episodes


def slack() -> list[Episode]:
    root = DATA_DIR / "slack"
    users = {u["id"]: u for u in json.loads((root / "users.json").read_text())}
    directory = "\n".join(
        f"- {u['profile']['display_name']} (@{u['name']}) is {u['real_name']}, {u['profile']['title']}"
        for u in users.values()
    )
    episodes = [Episode("slack/users.json", "slack", f"Slack member directory for the Orbisa workspace:\n{directory}",
                        EpisodeType.text, _utc("2026-01-01", "%Y-%m-%d"), "Slack member directory", "slack/users.json")]
    for path in sorted(root.glob("*/*.json")):
        channel, day = path.parent.name, path.stem
        messages = json.loads(path.read_text())
        lines = []
        for m in messages:
            who = users[m["user"]]["profile"]["display_name"]
            reply = " (thread reply)" if m.get("thread_ts") and m["thread_ts"] != m["ts"] else ""
            stamp = datetime.fromtimestamp(float(m["ts"]), tz=timezone.utc).strftime("%H:%M")
            lines.append(f"{who}{reply} [{stamp} UTC]: {m['text']}")
        start = datetime.fromtimestamp(float(messages[0]["ts"]), tz=timezone.utc)
        episodes.append(Episode(_rel(path), "slack", "\n".join(lines), EpisodeType.message, start,
                                f"Slack channel #{channel} on {day}", _rel(path)))
    return episodes


def drive() -> list[Episode]:
    episodes = []
    for path in sorted((DATA_DIR / "drive").glob("*.pdf")):
        text = "\n".join(page.extract_text() for page in PdfReader(path).pages)
        found = re.search(r"\d{4}-\d{2}-\d{2}", path.name) or re.search(r"\d{4}-\d{2}-\d{2}", text)
        signed = _utc(found.group(0), "%Y-%m-%d")
        body = f"Signed contract document from Google Drive: {path.stem.replace('_', ' ')}\n\n{text}"
        episodes.append(Episode(_rel(path), "drive", body, EpisodeType.text, signed,
                                f"Google Drive contract PDF '{path.name}'", _rel(path)))
    return episodes


def hubspot() -> list[Episode]:
    root = DATA_DIR / "hubspot"
    read = lambda name: list(csv.DictReader((root / name).open(newline="")))
    deals, contacts = defaultdict(list), defaultdict(list)
    for d in read("deals.csv"):
        deals[d["Associated Company"]].append(d)
    for c in read("contacts.csv"):
        contacts[c["Associated Company"]].append(c)
    episodes = []
    for company in read("companies.csv"):
        name = company["Company name"]
        payload = {"source": "HubSpot CRM export", "company": company, "deals": deals[name], "contacts": contacts[name]}
        episodes.append(Episode(f"hubspot/companies.csv#{company['Record ID']}", "hubspot", json.dumps(payload),
                                EpisodeType.json, _utc(company["Last Modified Date"], "%Y-%m-%d"),
                                f"HubSpot CRM record for {name} with deals and contacts", "hubspot/companies.csv"))
    return episodes


def zendesk() -> list[Episode]:
    """One episode per ticket per day, so a question asked as of a date never sees later comments."""
    root = DATA_DIR / "zendesk"
    people = json.loads((root / "users.json").read_text())
    users = {u["id"]: u["name"] for u in people["users"]}
    orgs = {o["id"]: o["name"] for o in people["organizations"]}
    episodes = []
    for t in json.loads((root / "tickets.json").read_text())["tickets"]:
        comments = json.loads((root / "comments" / f"{t['id']}.json").read_text())["comments"]
        by_day: dict[str, list[dict]] = defaultdict(list)
        for c in comments:
            by_day[c["created_at"][:10]].append(c)
        days = sorted(by_day)
        for day in days:
            header = (f"Zendesk ticket #{t['id']} from {orgs.get(t['organization_id'], 'unknown')}: {t['subject']} "
                      f"(opened {t['created_at'][:10]}, priority {t['priority']}). Activity on {day}:")
            lines = [header] + [
                f"{users[c['author_id']]}{'' if c['public'] else ' (internal note)'} [{c['created_at']}]: {c['body']}"
                for c in by_day[day]
            ]
            if day == days[-1] and t["updated_at"][:10] == day:
                lines.append(f"Ticket state at {t['updated_at']}: status {t['status']}, assignee "
                             f"{users[t['assignee_id']]}, tags {', '.join(t['tags'])}.")
            episodes.append(Episode(f"zendesk/tickets.json#{t['id']}@{day}", "zendesk", "\n".join(lines),
                                    EpisodeType.message, _iso(by_day[day][0]["created_at"]),
                                    f"Zendesk support ticket #{t['id']} activity on {day}",
                                    f"zendesk/comments/{t['id']}.json"))
    return episodes


def gong() -> list[Episode]:
    root = DATA_DIR / "gong"
    calls = {c["metaData"]["id"]: c for c in json.loads((root / "calls.json").read_text())["calls"]}
    episodes = []
    for tr in json.loads((root / "transcripts.json").read_text())["callTranscripts"]:
        call = calls[tr["callId"]]
        meta = call["metaData"]
        speakers = {p["speakerId"]: p for p in call["parties"]}
        roster = "; ".join(f"{p['name']} ({p['title']}, {p['affiliation'].lower()})" for p in call["parties"])
        lines = [f"Gong call recording: {meta['title']} on {meta['started'][:10]}. Participants: {roster}."]
        for segment in tr["transcript"]:
            who = speakers[segment["speakerId"]]["name"]
            lines += [f"{who}: {s['text']}" for s in segment["sentences"]]
        episodes.append(Episode(f"gong/transcripts.json#{tr['callId']}", "gong", "\n".join(lines), EpisodeType.message,
                                _iso(meta["started"]), f"Gong call transcript '{meta['title']}'", "gong/transcripts.json"))
    return episodes


PARSERS = {
    "confluence": confluence,
    "notion": notion,
    "slack": slack,
    "drive": drive,
    "hubspot": hubspot,
    "zendesk": zendesk,
    "gong": gong,
}


def load_episodes(systems: list[str] | None = None) -> list[Episode]:
    selected = systems or list(PARSERS)
    episodes = [ep for name in selected for ep in PARSERS[name]()]
    return sorted(episodes, key=lambda ep: (ep.reference_time, ep.name))
