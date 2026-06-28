extends Control
## PaxStressia — Godot 4 thin-client scaffold (read-only).
##
## Proves the contract in docs/CLIENT.md from a third client: load the JSON rules
## core (with §18.9 scenario layering), then render the starting state in plain
## words (§13.3). This is a SKELETON — it displays state, it does not yet run the
## turn loop. UNVERIFIED: authored without a Godot binary; open in Godot 4.x to
## validate. Touches nothing in sim/ or proto/.

const RULES_DIR := "res://rules/"
const RULE_FILES := ["nodes", "edges", "factions", "initiatives", "events", "constants", "patrons"]
const SCENARIO := "sahel_arc"

# Plain UI words over the model terms (the canonical map, docs/CLIENT.md §5).
const GOV_WORD := {
	"civilian": "elected", "junta": "military junta",
	"emirate": "insurgent-run", "failed": "collapsed",
}


func _ready() -> void:
	var rules := _load_rules(SCENARIO)
	if rules.is_empty():
		_show_error("No rules found under %s.\nCopy the repo's rules/ into client/godot/rules/ (see README.md)." % RULES_DIR)
		return
	_render(rules)


func _load_rules(scenario: String) -> Dictionary:
	var rules := {}
	for name in RULE_FILES:
		var data = _read_json(RULES_DIR + name + ".json")
		if data != null:
			rules[name] = data
	if rules.is_empty():
		return {}
	# Scenario layering (§18.9): scenario files REPLACE wholesale; constants MERGE.
	var sdir := RULES_DIR + "scenarios/" + scenario + "/"
	var scen = _read_json(sdir + "scenario.json")
	if scen != null:
		rules["scenario"] = scen
		for name in RULE_FILES:
			var data = _read_json(sdir + name + ".json")
			if data == null:
				continue
			if name == "constants":
				var merged: Dictionary = (rules.get("constants", {}) as Dictionary).duplicate()
				for k in data:
					merged[k] = data[k]
				rules["constants"] = merged
			else:
				rules[name] = data
	return rules


func _read_json(path: String):
	if not FileAccess.file_exists(path):
		return null
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return null
	var text := f.get_as_text()
	f.close()
	return JSON.parse_string(text)


func _render(rules: Dictionary) -> void:
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 6)
	col.position = Vector2(24, 24)
	add_child(col)

	var scen: Dictionary = rules.get("scenario", {})
	col.add_child(_label("PaxStressia — %s" % scen.get("name", SCENARIO), 24))
	col.add_child(_label("Godot client scaffold (read-only) — rendering the JSON core. See docs/CLIENT.md.", 12))

	# Starting standings, in plain words (§13.3).
	var starting: Dictionary = (rules.get("constants", {}) as Dictionary).get("starting", {})
	col.add_child(_label("\n🏠 Home %s     🤝 Allies %s     💰 Money %s" % [
		starting.get("domestic", "?"), starting.get("international", "?"), starting.get("treasury", "?")], 16))

	# The board: who rules + where the anger is (the eye finds the hot spots).
	var nodes: Array = rules.get("nodes", [])
	col.add_child(_label("\nRegions (%d):" % nodes.size(), 16))
	for n in nodes:
		var node: Dictionary = n
		col.add_child(_label("   %s — %s · Control %s · Anger %s" % [
			node.get("name", node.get("id", "?")),
			GOV_WORD.get(node.get("government", "civilian"), node.get("government", "?")),
			node.get("governance", "?"), node.get("grievance", "?")], 13))


func _label(text: String, size: int) -> Label:
	var lbl := Label.new()
	lbl.text = text
	lbl.add_theme_font_size_override("font_size", size)
	return lbl


func _show_error(msg: String) -> void:
	var lbl := _label(msg, 16)
	lbl.position = Vector2(24, 24)
	add_child(lbl)
