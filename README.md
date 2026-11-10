# alex-hw-reader

Personal, non-commercial, read-only Reddit reader for hardware hobby research.

- Reads this week's top posts and top comments from r/cyberDeck, r/hardwarehacking, r/SBCs, r/retrogaming, r/homelab
- Endpoints: `/r/{sub}/top?t=week`, `/comments/{id}` via application-only OAuth
- Read only: no posting, voting, messaging; under 500 requests/day; no resale or AI training

Usage: set `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`, then `pip install requests && python reader.py`.
