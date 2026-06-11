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

        # 6. List and Bullet Detection
        text = self.handle_lists(text)

        return text

    def handle_lists(self, text):
        """
        Converts phrases like "bullet [text]", "next point [text]", or 
        "list: item, item, item" into actual bulleted lists.
        """
        # 1. Handle explicit list triggers (e.g., "features: X, Y, Z" or "including X and Y")
        list_triggers = [
            r"points?:", r"bullet list:", r"list follows:", r"including:", 
            r"features?:", r"sections?:", r"items?:", r"components?:",
            r"that is", r"such as", r"namely"
        ]
        for trigger in list_triggers:
            # Check for trigger followed by colon or just a space if it's "that is/such as"
            pattern = rf"{trigger}[:\s]" if not trigger.endswith(":") else trigger
            match = re.search(pattern, text, re.IGNORECASE)
            
            if match:
                trigger_end = match.end()
                prefix = text[:trigger_end]
                list_part = text[trigger_end:]
                
                # Split by commas or "and" if it's a list-like structure (at least one comma or "and")
                if "," in list_part or " and " in list_part.lower():
                    items = re.split(r",\s*|\n|(?:\s+and\s+)", list_part, flags=re.IGNORECASE)
                    formatted_items = [f"• {i.strip().capitalize()}" for i in items if i.strip()]
                    
                    if len(formatted_items) > 1:
                        return prefix + "\n\n" + "\n\n".join(formatted_items)

        # 2. Handle inline bullet keywords (e.g., "I need bullet milk bullet eggs")
        # Supports "bullet", "point", "next point", "item"
        bullet_keywords = [r"\bbullet\b", r"\bnext point\b", r"\bpoint\b", r"\bitem\b"]
        
        # Use a regex to find all keyword occurrences
        combined_pattern = "|".join(bullet_keywords)
        
        if re.search(combined_pattern, text, re.IGNORECASE):
            # Split the text by these keywords
            parts = re.split(combined_pattern, text, flags=re.IGNORECASE)
            
            # If the first part is empty, the first word was a bullet
            # Otherwise, the first part is the intro text
            intro = parts[0].strip()
            if intro:
                new_text = intro + "\n\n"
            else:
                new_text = ""
                
            for part in parts[1:]:
                clean_part = part.strip()
                if clean_part:
                    # Clean up trailing punctuation since we're making it a list item
                    clean_part = clean_part.rstrip(".,")
                    new_text += f"• {clean_part.capitalize()}\n\n"
            
            return new_text.strip()

        # 3. Handle sequential enumeration (e.g., "First... Second... Third...")
        if text.lower().startswith("first "):
            text = "• " + text[6:].capitalize()
            # If there are "second", "third", etc. in the same text
            text = re.sub(r"\s+second\s+", "\n\n• ", text, flags=re.IGNORECASE)
            text = re.sub(r"\s+third\s+", "\n\n• ", text, flags=re.IGNORECASE)

        return text
