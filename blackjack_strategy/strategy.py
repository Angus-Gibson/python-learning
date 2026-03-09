# ─────────────────────────────────────────────
# BLACKJACK STRATEGY DATA
# Double-Deck, Dealer Hits Soft 17
# Keys: (player_hand, dealer_up)  Values: action
# ─────────────────────────────────────────────

DEALER_CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']

ACTION_COLORS = {
    'Hit':         '#F5C518',   # gold-yellow
    'Stand':       '#4CAF50',   # green
    'Double Down': '#E53935',   # red
    'Split':       '#1E88E5',   # blue
}

ACTION_SHORT = {
    'Hit': 'H', 'Stand': 'S', 'Double Down': 'D', 'Split': 'SP'
}


def build_strategy():
    """
    Build the complete blackjack basic strategy table for double-deck games
    where the dealer hits on soft 17.
    
    Returns:
        dict: Keys are tuples of (player_hand_label, dealer_up_card),
              Values are recommended actions (Hit, Stand, Double Down, Split)
    """
    table = {}

    # ── Section I: Hard Totals ──────────────────────────────────
    for d in DEALER_CARDS:
        table[('17+', d)] = 'Stand'

    s16 = {'2','3','4','5','6'}
    for d in DEALER_CARDS:
        table[('16', d)] = 'Stand' if d in s16 else 'Hit'

    for hand in ('15', '14', '13'):
        for d in DEALER_CARDS:
            table[(hand, d)] = 'Stand' if d in s16 else 'Hit'

    s12 = {'4','5','6'}
    for d in DEALER_CARDS:
        table[('12', d)] = 'Stand' if d in s12 else 'Hit'

    for d in DEALER_CARDS:
        table[('11', d)] = 'Double Down'

    d10_dd = {'2','3','4','5','6','7','8','9'}
    for d in DEALER_CARDS:
        table[('10', d)] = 'Double Down' if d in d10_dd else 'Hit'

    d9_dd = {'3','4','5','6'}
    for d in DEALER_CARDS:
        table[('9', d)] = 'Double Down' if d in d9_dd else 'Hit'

    for d in DEALER_CARDS:
        table[('5-8', d)] = 'Hit'

    # ── Section III: Soft Totals ────────────────────────────────
    for d in DEALER_CARDS:
        table[('A,9 / A,10', d)] = 'Stand'

    a8_d = {'6'}
    for d in DEALER_CARDS:
        table[('A,8', d)] = 'Double Down' if d in a8_d else 'Stand'

    a7_stand = {'7','8'}
    a7_dd    = {'2','3','4','5','6'}
    for d in DEALER_CARDS:
        if d in a7_stand:
            table[('A,7', d)] = 'Stand'
        elif d in a7_dd:
            table[('A,7', d)] = 'Double Down'
        else:
            table[('A,7', d)] = 'Hit'

    a6_dd = {'3','4','5','6'}
    for d in DEALER_CARDS:
        table[('A,6', d)] = 'Double Down' if d in a6_dd else 'Hit'

    a45_dd = {'4','5','6'}
    for hand in ('A,5', 'A,4'):
        for d in DEALER_CARDS:
            table[(hand, d)] = 'Double Down' if d in a45_dd else 'Hit'

    a23_dd = {'4','5','6'}
    for hand in ('A,3', 'A,2'):
        for d in DEALER_CARDS:
            table[(hand, d)] = 'Double Down' if d in a23_dd else 'Hit'

    # ── Section IV: Pairs ───────────────────────────────────────
    for d in DEALER_CARDS:
        table[('A,A / 8,8', d)] = 'Split'

    for d in DEALER_CARDS:
        table[('10,10', d)] = 'Stand'

    for d in DEALER_CARDS:
        table[('9,9', d)] = 'Stand' if d in {'7','10','A'} else 'Split'

    sp77 = {'2','3','4','5','6','7'}
    for d in DEALER_CARDS:
        table[('7,7', d)] = 'Split' if d in sp77 else 'Hit'

    sp66 = {'2','3','4','5','6'}
    for d in DEALER_CARDS:
        table[('6,6', d)] = 'Split' if d in sp66 else 'Hit'

    d55_dd = {'2','3','4','5','6','7','8','9'}
    for d in DEALER_CARDS:
        table[('5,5', d)] = 'Double Down' if d in d55_dd else 'Hit'

    sp44 = {'5','6'}
    for d in DEALER_CARDS:
        table[('4,4', d)] = 'Split' if d in sp44 else 'Hit'

    sp33 = {'2','3','4','5','6','7'}
    for d in DEALER_CARDS:
        table[('3,3', d)] = 'Split' if d in sp33 else 'Hit'

    sp22 = {'2','3','4','5','6','7'}
    for d in DEALER_CARDS:
        table[('2,2', d)] = 'Split' if d in sp22 else 'Hit'

    return table


# Load the strategy table
STRATEGY = build_strategy()


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
