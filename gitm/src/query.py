import sys
import json

emojis = {
    "chore": "🎨",
    "docs": "📝",
    "feat": "✨",
    "fix": "🐛",
    "refactor": "♻️",
    "style": "💄",
    "test": "✅"
}

query = sys.argv[1:]
action = query[0]
is_action_valid = action in emojis


_default = [{
    "title": "valid types: {lst}".format(lst=", ".join(emojis.keys()))
}]


def get_items(q):

    all_suggestions = [{
        "title": "{key}: {value}".format(key=key, value=emojis[key]),
        "autocomplete": "{key} ".format(key=key)
    } for key in emojis.keys()]

    filtered_suggestions = [suggestion for suggestion in all_suggestions if suggestion["title"].startswith(action)]
    default = filtered_suggestions if len(filtered_suggestions) > 0 else all_suggestions

    if not is_action_valid:
        return default

    if len(q) == 1:
        return [{
            "title": "{action}: {emoji} <commit message>".format(
                action=action,
                emoji=emojis.get(action)
            )
        }]

    title = "{action}: {emoji} {message}".format(
        action=action,
        emoji=emojis.get(action),
        message=" ".join(q[1:])
    )

    return [{
        "title": title,
        "subtitle": "Copy result to clipboard",
        "arg": title
    }]


result = json.dumps({
    "items": get_items(query)
}, indent=2)

sys.stdout.write(result)

