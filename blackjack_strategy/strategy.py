# ─────────────────────────────────────────────
# BLACKJACK STRATEGY DATA
# Double-Deck, Dealer Hits Soft 17
# Loaded from strategy.yaml configuration file
# ─────────────────────────────────────────────

import os
import yaml


def _load_yaml_config():
    """Load the strategy configuration from YAML file."""
    yaml_path = os.path.join(os.path.dirname(__file__), 'strategy.yaml')
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def _build_strategy_from_yaml(config):
    """
    Convert YAML strategy configuration into a lookup table.
    
    Returns:
        dict: Keys are tuples of (player_hand_label, dealer_up_card),
              Values are recommended actions (Hit, Stand, Double Down, Split)
    """
    table = {}
    dealer_cards = config['dealer_cards']
    
    # Process hard totals
    for hand, rules in config['hard_totals'].items():
        if 'dealers' in rules and rules['dealers'] == 'all':
            # Apply action to all dealer cards
            for d in dealer_cards:
                table[(hand, d)] = rules['action']
        else:
            # Conditional logic
            stand_against = set(rules.get('stand_against', []))
            double_against = set(rules.get('double_down_against', []))
            default = rules.get('default_action', 'Hit')
            
            for d in dealer_cards:
                if d in stand_against:
                    table[(hand, d)] = 'Stand'
                elif d in double_against:
                    table[(hand, d)] = 'Double Down'
                else:
                    table[(hand, d)] = default
    
    # Process soft totals
    for hand, rules in config['soft_totals'].items():
        if 'dealers' in rules and rules['dealers'] == 'all':
            for d in dealer_cards:
                table[(hand, d)] = rules['action']
        else:
            stand_against = set(rules.get('stand_against', []))
            double_against = set(rules.get('double_down_against', []))
            default = rules.get('default_action', 'Hit')
            
            for d in dealer_cards:
                if d in stand_against:
                    table[(hand, d)] = 'Stand'
                elif d in double_against:
                    table[(hand, d)] = 'Double Down'
                else:
                    table[(hand, d)] = default
    
    # Process pairs
    for hand, rules in config['pairs'].items():
        if 'dealers' in rules and rules['dealers'] == 'all':
            for d in dealer_cards:
                table[(hand, d)] = rules['action']
        else:
            stand_against = set(rules.get('stand_against', []))
            split_against = set(rules.get('split_against', []))
            default = rules.get('default_action', 'Hit')
            
            for d in dealer_cards:
                if d in stand_against:
                    table[(hand, d)] = 'Stand'
                elif d in split_against:
                    table[(hand, d)] = 'Split'
                else:
                    table[(hand, d)] = default
    
    return table


# Load configuration
_config = _load_yaml_config()

# Extract dealer cards and action metadata
DEALER_CARDS = _config['dealer_cards']
ACTION_COLORS = _config['action_colors']
ACTION_SHORT = _config['action_short']

# Build the strategy table
STRATEGY = _build_strategy_from_yaml(_config)


def make_cards():
    """
    Create a list of flashcard dictionaries from the strategy table.
    
    Returns:
        list: List of dicts with keys 'hand', 'dealer', and 'action'
    """
    cards = []
    for (hand, dealer), action in STRATEGY.items():
        cards.append({
            'hand':   hand,
            'dealer': dealer,
            'action': action,
        })
    return cards
