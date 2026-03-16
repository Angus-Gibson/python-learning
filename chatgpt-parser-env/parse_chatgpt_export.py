"""
ChatGPT Export Parser — Title-Based Classification (No API Required)
---------------------------------------------------------------------
Parses one or more ChatGPT conversations-NNN.json export files, classifies
each conversation by matching its title against keyword rules, then writes
one .txt file per theme plus Uncategorized.txt for anything unmatched.

Usage:
    python parse_chatgpt_export.py --input-dir /path/to/export --output ./output
"""

import argparse
import datetime
import glob
import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# Theme rules — ordered by priority (first match wins)
# ---------------------------------------------------------------------------

THEME_RULES = [
    ("Angusius and Calypso", [
        "angusius", "calypso", "ogygia", "ogygian", "odysseus calypso",
    ]),
    ("Greek Mythology and Odyssey", [
        "odysseus", "odyssey", "penelope", "iliad", "homeric", "hades",
        "persephone", "artemis", "athena", "apollo", "diomedes", "ithaca",
        "greek myth", "greek hospit", "greek epith", "greek self",
        "ancient greek", "trojans", "spartan", "shade's journey",
        "hades and greek", "epic the musical", "olive tree bed",
    ]),
    ("Faersch Saga", [
        "faersch", "elenwë", "hilinrónë", "lost child",
        "starting faersch", "himbo paladin",
    ]),
    ("Vampire the Masquerade", [
        "v5 lore", "v5 character", "v5 char", "mychal", "banu haqim",
        "camarilla", "anarch", "masquerade",
    ]),
    ("Mythology and Religion", [
        "kemetic", "dr. siuda", "brother adam", "faith and hypocrisy",
        "billy graham", "dietrich bonhoeffer", "protestant confes",
        "jesus and stoic", "god's gonna", "prophetic parallel",
        "ramin the reluctant", "lenin and socialist",
    ]),
    ("Stoic Philosophy", [
        "stoic", "marcus aurelius", "nietzsche", "cynicism vs", "daily stoic",
        "zen of python", "philosophy in prison", "philosophers chron",
        "socialist vs communist",
    ]),
    ("Sports", [
        "baseball", "cubs", "mlb", "cricket", "steve austin goat",
        "boston's perfect", "miracle on ice", "soviet hockey",
    ]),
    ("Music and Songwriting", [
        "song", "lyric", "guitar", "songwrit", "chord", "singing",
        "grunge", "chris cornell", "bon scott", "stairway",
        "nostalgia through music", "nostalgic song", "healing through music",
        "emotional power", "evoking chopin", "octave", "jam band",
        "polynesian singing", "sing like", "screech technique",
        "beatles", "mozart", "psychoderelict", "eclipse album", "iviiv",
        "romantic with classical", "candy candido", "earplug balance",
        "right-handed drummer", "pope rock band", "stokowski",
    ]),
    ("History and Military", [
        "1980 miracle", "1983 delorean", "1990s", "1998 american",
        "moon landing", "armistice", "july 20 plot", "nuclear",
        "vietnam", "ww2", "rommel", "speer", "saladin",
        "roman emperor", "roman empire", "roman names", "marc antony",
        "union soldiers", "eagle has landed", "seal team", "turing",
        "enigma", "miracle speech", "eugene fluckey", "ham radio rescue",
        "military protocol", "time travel to 1787", "détente",
        "ireland unif", "irish", "bathing the emperor",
        "emperor conversation", "endeavour call", "f-14", "f-15",
        "lieutenant's quick", "long thaw", "nasa astronaut",
        "notable bad presidents", "roosevelt political", "secret service",
        "cia moscow", "leonardo and renaissance", "july 20",
        "1980s combat", "apollo 13", "apollo lunar",
    ]),
    ("DevOps and Tech Career", [
        "devops", "linux", "python", "tech career", "tech solution",
        "best laptop", "path to senior", "ms in computer",
        "ai tools in devops", "ai defense", "cybersecurity",
        "chrome vs firefox", "arch linux", "why developers use linux",
        "linux cheat", "linux command", "linux network", "understanding linux",
        "medium subscription for python", "career pivot", "cover letter ramp",
        "ivy league alt", "backblaze", "aw3425", "better keyboard",
        "custom bedtime story app", "mental math", "misleading chart",
        "openai donations", "rust pc", "rust timeout", "rust upkeep",
        "samsung wallet", "t-mobile", "transfer openai", "using abacus",
        "vertical mice", "ai memory injection", "pc sleep",
    ]),
    ("Finance and Practical Life", [
        "cd ladder", "hysa", "bitcoin", "wealth gap", "high yield",
        "amex", "blackjack", "budget sound", "pricing model",
        "bar chicago", "buying a bar", "coca-cola market",
        "dishwasher filter", "evening wear", "home design",
        "illinois residency", "medicare cuts", "mid-century modern tv",
        "mildew removal", "twa hotel",
    ]),
    ("Health and Wellness", [
        "sleep", "fitness", "macro", "belly fat", "back acne", "foot disc",
        "hand tremor", "paxil", "ibs flare", "apnea", "tm for anxiety",
        "headbanging", "physiolog", "cuteness", "alt elevation",
        "best martial arts", "dreams and brain", "from sedentary",
    ]),
    ("Creative Writing", [
        "creative writing", "creative role", "story feedback", "scene analysis",
        "scene rewrite", "polished", "style contrast",
        "historical short story", "stand-up routine", "comedy script",
        "memoir", "buddy cop", "interrogation room", "director's office",
        "debugging and supernatural", "mission dialogue", "trope origins",
        "rust revenge", "the wolf", "labyrinth of love", "dance with jordan",
        "wake-up call fantasy", "angus gibson", "gibson's game", "karlach",
        "doppelganger", "cat relaxation", "compelling husband",
        "epic rap battle", "falcon maintenance", "guardians against night",
        "lion rumble", "no respect routine", "prince's dilemma",
        "vivi's cat", "your curse", "book title",
    ]),
    ("Pop Culture and Media", [
        "batman", "star wars", "terminator", "tmnt", "metal gear",
        "hal 9000", "charlotte's web", "monsters inc", "west wing",
        "mandy in the west", "mrs. landingham", "tom branson",
        "downton", "survivor", "no man's sky", "fallout",
        "late night comedy", "corporate satire", "luke and the dark",
        "doc holliday", "grunge kindness", "grunge legends",
        "gimli encounter", "hannibal lecter", "norm's heavenly",
        "reconciling lovecraft", "why care about gatsby",
    ]),
    ("Personal Reflection and Grief", [
        "grief", "grieving", "uncle robert", "fear of losing dad",
        "painful memories", "missing saimy", "pet rats",
        "family dynamics", "attraction to powerful", "dream analysis",
        "stammering", "motivation", "becoming laconic", "becoming a great",
        "love and discipline", "freedom and service", "human traits",
        "heroic inspirations", "myself and my friends", "political recal",
        "boredom breakthrough", "uncanny valley", "ali's encouragement",
        "betrayal at work", "email to dr. wilson", "honoring sacred",
        "letter to professor", "making it official", "police accountability",
        "profile refinement", "steve irwin", "we'll see",
    ]),
    ("Food and Drink", [
        "whiskey", "barrel", "vodka", "guinness", "cocktail", "recipe",
        "aging whiskey", "best barrel", "mead", "chef ramsey",
        "thanksgiving reimagined", "cookunity", "cook unity", "uber eats",
        "polite recipe",
    ]),
    ("Language and Culture", [
        "arabic", "cherokee", "japanese", "日本", "asl", "lingopie",
        "linguistic", "haka", "polynesian", "irish toast",
        "head coverings",
    ]),
]

# Manual overrides for titles that don't pattern-match well
MANUAL_OVERRIDES = {
    # Previous fixes
    "Rust Revenge Saga": "Creative Writing",
    "Rust PC Optimization Guide": "DevOps and Tech Career",
    "Rust Timeout Diagnosis": "DevOps and Tech Career",
    "Rust Upkeep Calculation": "DevOps and Tech Career",
    "No Man's Sky 2026 Goals": "Pop Culture and Media",
    "1980s Combat Air Patrol": "History and Military",
    "Apollo 13 Explosive Glitch": "History and Military",
    "Apollo Lunar Surface Contact": "History and Military",
    "Starting Faersch's Novel": "Faersch Saga",
    # Greek Mythology
    "Myself and My Greek Pantheon": "Greek Mythology and Odyssey",
    "Reimagining the Judgement of Paris": "Greek Mythology and Odyssey",
    "Adopting Hestia tips": "Greek Mythology and Odyssey",
    # History and Military
    "Washington returns Howe's dog": "History and Military",
    "Caesar and Augustus rulers": "History and Military",
    "Marie Antoinette execution debate": "History and Military",
    "TCS footage 1981 Gulf": "History and Military",
    "Miracle at South Bend": "History and Military",
    "US intelligence data analysis": "History and Military",
    "Gaza flotilla situation": "History and Military",
    "1998 as American peak": "History and Military",
    # Mythology and Religion
    "Moses name origin": "Mythology and Religion",
    "Mary as a mother": "Mythology and Religion",
    "Faith and dissonance": "Mythology and Religion",
    "TM with ADHD and Christianity": "Mythology and Religion",
    # Stoic Philosophy
    "Orwell vs Huxley themes": "Stoic Philosophy",
    "Matrix freedom debate": "Stoic Philosophy",
    "Empathy and hypocrisy debate": "Stoic Philosophy",
    "Art vs artist struggle": "Stoic Philosophy",
    "Progressive vs Establishment Dems": "Stoic Philosophy",
    # Creative Writing
    "Immersive narrative continuation": "Creative Writing",
    "Injury adds emotional punch": "Creative Writing",
    "Fiction writing tools": "Creative Writing",
    "Air Support for Fellowship": "Creative Writing",
    "Scene refinement suggestions": "Creative Writing",
    "Belmont diary analysis": "Creative Writing",
    "Lenore and Hector's relationship": "Creative Writing",
    "Field diary excerpt": "Creative Writing",
    "Cyberpunk vignette feedback": "Creative Writing",
    "Parody verse help": "Creative Writing",
    "Poem analysis and feedback": "Creative Writing",
    "Polishing a narrative": "Creative Writing",
    "Radio Drama Feedback": "Creative Writing",
    # Pop Culture and Media
    "Mother Gothel's Love Debate": "Pop Culture and Media",
    "Jedi Oath Rejected": "Pop Culture and Media",
    "Mjoll the Lioness wife goals": "Pop Culture and Media",
    "D&D Paladin Comparison": "Pop Culture and Media",
    "Real-life Sister Georges": "Pop Culture and Media",
    "Papal feline proclamation": "Pop Culture and Media",
    # Music and Songwriting
    "Feelin' This anthem argument": "Music and Songwriting",
    "Karaoke memory reflection": "Music and Songwriting",
    "Ozzy addiction insight": "Music and Songwriting",
    # Sports
    "2016 World Series drama": "Sports",
    "Peyton Manning decision": "Sports",
    "Football defense discussion": "Sports",
    "Choking up vs hands low": "Sports",
    # Health and Wellness
    "Nocturia causes at 35": "Health and Wellness",
    "Elliptical workout evaluation": "Health and Wellness",
    "Cannabis and depression impact": "Health and Wellness",
    "Cannabis and thought speed": "Health and Wellness",
    "Kneeling rise stunt technique": "Health and Wellness",
    "Lowering speaking voice": "Health and Wellness",
    # DevOps and Tech Career
    "Windows reinstall guide": "DevOps and Tech Career",
    "Mod error check": "DevOps and Tech Career",
    "Various PC discussion": "DevOps and Tech Career",
    "Skyrim CTD troubleshooting": "DevOps and Tech Career",
    "Setup for voice over": "DevOps and Tech Career",
    "UTK Computer Science Admission": "DevOps and Tech Career",
    # Finance and Practical Life
    "Headphones comparison Heavys vs Sony": "Finance and Practical Life",
    "Sunglasses for different occasions": "Finance and Practical Life",
    "Zippo fuel evaporation explanation": "Finance and Practical Life",
    "Extending liqueur shelf life": "Food and Drink",
    "Pocket watch repair cost": "Finance and Practical Life",
    "Easing back to work": "Finance and Practical Life",
    # Personal Reflection and Grief
    "Flirting with strangers": "Personal Reflection and Grief",
    "Perfect woman for you": "Personal Reflection and Grief",
    "Dreams of past homes": "Personal Reflection and Grief",
    "Meeting women in Chicago": "Personal Reflection and Grief",
    "James Lipton questionnaire": "Personal Reflection and Grief",
    "Enneagram type analysis": "Personal Reflection and Grief",
    "Decision between events": "Personal Reflection and Grief",
    "We'll See": "Personal Reflection and Grief",
    # Language and Culture
    "Arab nickname suggestions": "Language and Culture",
    "Scottish slang message": "Language and Culture",
    "Keffiyeh procurement and wear": "Language and Culture",
    "French language upload": "Language and Culture",
    "Native American ancestry search": "Language and Culture",
    "Solidarity flyer tips": "Language and Culture",
    # Misc / truly uncategorized
    "Dinosaur intelligence milestones": "Uncategorized",
    "Orange and white daisies": "Uncategorized",
    "Image Request": "Uncategorized",
    "Article Explanation Request": "Uncategorized",
    "Explain legal exchange": "Uncategorized",
    "Judge bias response options": "Uncategorized",
    "Conversation transcript analysis": "Uncategorized",
}


def classify_by_title(title: str) -> str:
    if title in MANUAL_OVERRIDES:
        return MANUAL_OVERRIDES[title]
    lower = title.lower()
    for theme_label, keywords in THEME_RULES:
        for kw in keywords:
            if kw.lower() in lower:
                return theme_label
    return "Uncategorized"


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_all_conversations(input_dir: str) -> list:
    pattern = os.path.join(input_dir, "conversations*.json")
    files = sorted(glob.glob(pattern))

    if not files:
        if os.path.isfile(input_dir) and input_dir.endswith(".json"):
            files = [input_dir]
        else:
            print(f"ERROR: No conversations*.json files found in: {input_dir}")
            sys.exit(1)

    all_convos = []
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            all_convos.extend(data)
        elif isinstance(data, dict):
            for key in ("conversations", "data", "items"):
                if key in data and isinstance(data[key], list):
                    all_convos.extend(data[key])
                    break

    print(f"Loaded {len(all_convos)} conversations from {len(files)} file(s).")
    return all_convos


# ---------------------------------------------------------------------------
# Message extraction
# ---------------------------------------------------------------------------

def _extract_text(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, dict):
        parts = content.get("parts", [])
        return " ".join(str(p) for p in parts if isinstance(p, str)).strip()
    return ""


def extract_messages(conversation: dict) -> list:
    mapping = conversation.get("mapping", {})
    if not mapping:
        return []

    current_node = conversation.get("current_node")
    if not current_node:
        return []

    path = []
    node_id = current_node
    visited = set()
    while node_id and node_id not in visited:
        visited.add(node_id)
        path.append(node_id)
        node = mapping.get(node_id, {})
        node_id = node.get("parent")
    path.reverse()

    messages = []
    for nid in path:
        node = mapping.get(nid, {})
        msg = node.get("message")
        if not msg:
            continue
        role = msg.get("author", {}).get("role", "")
        if role not in ("user", "assistant"):
            continue
        text = _extract_text(msg.get("content", {}))
        if text:
            messages.append({"role": role, "text": text})

    return messages


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_conversation(conversation: dict, messages: list) -> str:
    title = conversation.get("title", "Untitled")
    create_time = conversation.get("create_time")
    date_str = ""
    if create_time:
        try:
            dt = datetime.datetime.fromtimestamp(float(create_time))
            date_str = dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    lines = ["=" * 60, f"CONVERSATION: {title}"]
    if date_str:
        lines.append(f"DATE: {date_str}")
    lines += ["=" * 60, ""]

    for msg in messages:
        label = "Me" if msg["role"] == "user" else "ChatGPT"
        lines.append(f"[{label}]")
        lines.append(msg["text"])
        lines.append("")

    lines.append("")
    return "\n".join(lines)


def safe_filename(label: str) -> str:
    name = re.sub(r"[^\w\s-]", "", label).strip()
    name = re.sub(r"\s+", "_", name)
    return name or "Uncategorized"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Parse ChatGPT export into themed .txt files (title-based)."
    )
    parser.add_argument(
        "--input-dir", required=True,
        help="Directory containing conversations-NNN.json files"
    )
    parser.add_argument(
        "--output", default="./output",
        help="Directory for output .txt files (default: ./output)"
    )
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    conversations = load_all_conversations(args.input_dir)
    total = len(conversations)
    print(f"\nClassifying {total} conversation(s) by title...\n")

    theme_buckets = {}

    for i, convo in enumerate(conversations, 1):
        title = convo.get("title", "Untitled")
        theme = classify_by_title(title)
        print(f"[{i}/{total}] {title[:60]:<60} -> {theme}")

        messages = extract_messages(convo)
        if not messages:
            continue

        formatted = format_conversation(convo, messages)
        theme_buckets.setdefault(theme, []).append(formatted)

    print(f"\nWriting files to: {args.output}/\n")
    for theme, blocks in sorted(theme_buckets.items()):
        filename = safe_filename(theme) + ".txt"
        filepath = os.path.join(args.output, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"THEME: {theme}\n")
            f.write(f"CONVERSATIONS IN THIS FILE: {len(blocks)}\n")
            f.write("=" * 60 + "\n\n")
            for block in blocks:
                f.write(block)
        print(f"  -> {filename}  ({len(blocks)} conversation(s))")

    print(f"\nDone! {len(theme_buckets)} theme file(s) written.")


if __name__ == "__main__":
    main()
