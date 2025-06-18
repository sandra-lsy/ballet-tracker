import json

class BalletSearchEngine:
    def __init__(self, ballets_data):
        self.ballets = ballets_data
        # Built-in terminology
        self.variation_keywords = {
            'variation': ['variation', 'solo', 'dance'],
            'pas_de_deux': ['pas de deux', 'duet', 'partnership'],
            'pas_de_trois': ['pas de trois', 'trio'],
            'corps_de_ballet': ['corps', 'ensemble', 'group'],
            'grand_pas': ['grand pas', 'finale']
        }

        # Common scenes
        self.scene_patterns = {
            'wedding': ['wedding', 'marriage'],
            'death': ['death', 'tragic', 'ending'],
            'transformation': ['transformation', 'curse', 'spell'],
            'dream': ['dream', 'fantasy', 'vision'],
        }

    def build_search_query(self, ballet_key, **kwargs):
        """Generate one custom search query based on user input"""
        ballet = self.ballets[ballet_key]
        terms = [f"{ballet['title']} ballet"]

        # Add main characters
        if kwargs.get('character'):
            char = kwargs['character']
            if char in ballet['main_characters']:
                terms.append(char)
            terms.append(char)

        # Add acts with standard roman numerals
        if kwargs.get('acts'):
            act_num = kwargs['acts']
            terms.extend([f"Act {act_num}", f"Act {self._to_roman(act_num)}"])

        # Scene type with built-in terms
        if kwargs.get('scene_type'):
            scene = kwargs['scene_type'].lower()
            if scene in self.variation_keywords:
                terms.extend(self.variation_keywords[scene])
        
        # Company and extra info
        if kwargs.get('company'):
            terms.append(kwargs['company'])

        if kwargs.get('extras'):
            terms.append(kwargs['extras'])

        return ' '.join(set(terms)) # remove duplicates
    
    def _to_roman(self, n):
        """Convert integer to Roman numeral"""
        vals = [10, 9, 5, 4, 1]
        syms = ['X', 'IX', 'V', 'IV', 'I']
        roman_num = ''
        for i in range(len(vals)):
            count = int(n / vals[i])
            roman_num += syms[i] * count
            n -= vals[i] * count
        return roman_num
    
    def suggest_searches(self, ballet_key):
        """Generate common search options for user to choose from"""
        ballet = self.ballets[ballet_key]
        suggestions = []

        # Character-specific search for main characters
        for char in ballet['main_characters']:
            suggestions.append(self.build_search_query(ballet_key, character=char, scene_type='variation'))

        # Act-specific searches
        for act in range(1, ballet['acts'] + 1):
            suggestions.append(self.build_search_query(ballet_key, acts=act))

        # Pas de deux and pas de trois
        if len(ballet['main_characters']) == 2:
            suggestions.append(
                self.build_search_query(ballet_key, scene_type='pas_de_deux')
            )
        elif len(ballet['main_characters']) == 3:
            suggestions.append(
                self.build_search_query(ballet_key, scene_type='pas_de_trois')
            )

        return suggestions

    def build_default_search_query(self, ballet_key):
        """Generate default search query for each ballet"""
        ballet = self.ballets[ballet_key]
        terms = [f"{ballet['title']} ballet"]
        
        return " ".join(set(terms))