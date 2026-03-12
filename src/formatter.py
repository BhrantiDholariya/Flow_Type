import re

class TextFormatter:
    def __init__(self, config=None):
        self.config = config or {}
        self.emoji_map = {
            "heart emoji": "❤️",
            "laughing emoji": "😂",
            "smiley face": "😊",
            "thumbs up": "👍",
            "rocket emoji": "🚀",
            "fire emoji": "🔥",
            "check mark": "✅",
            "cross mark": "❌",
            "thinking emoji": "🤔",
            "party emoji": "🎉",
        }
        
        self.fillers = [
            r"\bumm\b", r"\buhh\b", r"\bahh\b", r"\blike\b", r"\bu know\b", 
            r"\byou know\b", r"\bi mean\b", r"\berr\b"
        ]

        self.corrections = {
            # Jio Corrections
            r"\bGeo\b": "Jio",
            r"\bT your\b": "Jio",
            r"\bG-O\b": "Jio",
            r"\bJoe\b": "Jio",
            r"\bGio\b": "Jio",
            r"\bGieo\b": "Jio",
            
            # Hotstar Corrections
            r"\bhot stuff\b": "Hotstar",
            r"\bhot star\b": "Hotstar",
            r"\bhostar\b": "Hotstar",
            r"\bhostas\b": "Hotstar",
            r"\bhotster\b": "Hotstar",
            
            # WhatsApp Corrections
            r"\bwhat's up\b": "WhatsApp",
            r"\bwhat sap\b": "WhatsApp",
            r"\bwatsapp\b": "WhatsApp",
            r"\bwhat's app\b": "WhatsApp",
            r"\bwats up\b": "WhatsApp",
            r"\bwhats app\b": "WhatsApp",
        }

    def format(self, text):
        if not text:
            return ""

        # 0. Apply Brand Corrections
        for pattern, replacement in self.corrections.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # 1. Cleanup filler words
        if self.config.get("remove_fillers", True):
            for filler in self.fillers:
                text = re.sub(filler, "", text, flags=re.IGNORECASE)

        # 2. Cleanup extra spaces
        text = " ".join(text.split())

        # 3. Capitalize first letter
        if self.config.get("auto_capitalize", True):
            if text:
                text = text[0].upper() + text[1:]

        # 4. Handle Emojis
        if self.config.get("convert_emojis", True):
            for keyword, emoji in self.emoji_map.items():
                text = re.sub(rf"\b{keyword}\b", emoji, text, flags=re.IGNORECASE)

        # 5. Rule-based Punctuation (Basic)
        if self.config.get("auto_punctuate", True):
            if text and text[-1] not in ".!?":
                text += "."

        # 6. Basic Bullet Detection
        # Convert "First ... Second ... Third ..." to list items if they are at start
        # This is a bit complex for rule-based, but let's do a simple version
        if text.lower().startswith("first "):
            text = "• " + text[6:]
        
        return text
