from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# ------------- JSON HELPERS -------------

def load_json(filename, default):
    if not os.path.exists(filename):
        return default
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ------------- PUBLIC PAGES -------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/league")
def league():
    table = load_json("table.json", {})
    return render_template("league.html", table=table)

@app.route("/fixtures")
def fixtures():
    fixtures = load_json("fixtures.json", [])
    return render_template("fixtures.html", fixtures=fixtures)

@app.route("/teams")
def teams():
    teams = load_json("teams.json", [])
    return render_template("teams.html", teams=teams)

@app.route("/squads")
def squads():
    players = load_json("players.json", [])
    teams = load_json("teams.json", [])
    return render_template("squads.html", players=players, teams=teams)

@app.route("/transfers")
def transfers():
    transfers = load_json("transfers.json", [])
    return render_template("transfers.html", transfers=transfers)

# ------------- ADMIN DASHBOARD -------------

@app.route("/admin")
def admin():
    return render_template("admin.html")

# Stats Manager
@app.route("/admin/stats-manager")
def admin_stats_manager():
    return render_template("admin_stats_manager.html")

# Players
@app.route("/admin/players")
def admin_players():
    return render_template("admin_players.html")

# Analytics
@app.route("/admin/analytics")
def admin_analytics():
    return render_template("admin_analytics.html")

# Transfers (admin view)
@app.route("/admin/transfers")
def admin_transfers():
    transfers = load_json("transfers.json", [])
    return render_template("admin_transfers.html", transfers=transfers)

# Matches
@app.route("/admin/matches")
def admin_matches():
    return render_template("admin_matches.html")

# Competitions
@app.route("/admin/competitions")
def admin_competitions():
    return render_template("admin_competitions.html")

# Ballon d'Or
@app.route("/admin/ballon")
def admin_ballon():
    return render_template("admin_ballon.html")

# Audit Logs
@app.route("/admin/audit-logs")
def admin_audit_logs():
    return render_template("admin_audit_logs.html")

# Settings
@app.route("/admin/settings")
def admin_settings():
    return render_template("admin_settings.html")

# ------------- TROPHIES -------------

@app.route("/admin/trophies")
def admin_trophies():
    trophies = load_json("trophies.json", [])
    return render_template("admin_trophies.html", trophies=trophies)

@app.route("/admin/trophies/add", methods=["POST"])
def admin_add_trophy():
    trophies = load_json("trophies.json", [])

    new_trophy = {
        "icon": request.form.get("icon", "").strip(),
        "team": request.form.get("team", "").strip(),
        "title": request.form.get("title", "").strip(),
        "season": request.form.get("season", "").strip(),
        "date": request.form.get("date", "").strip()
    }

    trophies.append(new_trophy)
    save_json("trophies.json", trophies)

    return redirect(url_for("admin_trophies"))

@app.route("/admin/trophies/delete/<int:index>", methods=["POST"])
def admin_delete_trophy(index):
    trophies = load_json("trophies.json", [])
    if 0 <= index < len(trophies):
        trophies.pop(index)
        save_json("trophies.json", trophies)
    return redirect(url_for("admin_trophies"))

# ------------- EDIT TEAMS (EXISTING) -------------

@app.route("/admin/edit-teams", methods=["GET", "POST"])
def admin_edit_teams():
    teams = load_json("teams.json", [])
    if request.method == "POST":
        raw = request.form.get("teams_json", "")
        try:
            new_data = json.loads(raw)
            save_json("teams.json", new_data)
            teams = new_data
        except Exception:
            pass
    return render_template("admin_edit_teams.html", teams=teams)

# ------------- RUN -------------

if __name__ == "__main__":
    app.run(debug=True)
