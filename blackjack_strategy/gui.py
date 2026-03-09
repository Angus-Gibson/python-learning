import tkinter as tk
import random
from strategy import DEALER_CARDS, ACTION_COLORS, ACTION_SHORT, STRATEGY, make_cards


class BlackjackFlashcardApp:
    """GUI application for blackjack strategy flashcards."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Strategy Flashcards")
        self.root.configure(bg='#0A1628')
        self.root.resizable(False, False)

        self.cards = make_cards()
        random.shuffle(self.cards)
        self.index = 0
        self.flipped = False
        self.score = {'correct': 0, 'wrong': 0, 'seen': 0}

        self._build_ui()
        self._show_card()

    # ── UI Construction ──────────────────────────────────────────
    def _build_ui(self):
        """Build the complete user interface."""
        W = 560
        PAD = 28

        # Title bar
        title_frame = tk.Frame(self.root, bg='#0A1628')
        title_frame.pack(fill='x', padx=PAD, pady=(PAD, 0))

        title_lbl = tk.Label(
            title_frame, text='♠  BLACKJACK STRATEGY  ♠',
            font=('Georgia', 15, 'bold'), fg='#C9A84C', bg='#0A1628'
        )
        title_lbl.pack()

        subtitle = tk.Label(
            title_frame, text='Double Deck · Dealer Hits Soft 17',
            font=('Georgia', 9, 'italic'), fg='#7A8BA0', bg='#0A1628'
        )
        subtitle.pack()

        # Progress bar area
        prog_frame = tk.Frame(self.root, bg='#0A1628')
        prog_frame.pack(fill='x', padx=PAD, pady=(10, 0))

        self.progress_lbl = tk.Label(
            prog_frame, text='', font=('Courier', 10),
            fg='#7A8BA0', bg='#0A1628'
        )
        self.progress_lbl.pack(side='left')

        self.score_lbl = tk.Label(
            prog_frame, text='', font=('Courier', 10),
            fg='#7A8BA0', bg='#0A1628'
        )
        self.score_lbl.pack(side='right')

        # Card canvas ─ felt green table surface
        self.canvas = tk.Canvas(
            self.root, width=W, height=260,
            bg='#0A1628', highlightthickness=0
        )
        self.canvas.pack(padx=PAD, pady=12)

        # Card background (rounded rect via polygon)
        self._draw_card_bg()

        # Front: player hand labels
        self.lbl_front_top = tk.Label(
            self.canvas, text='YOUR HAND',
            font=('Georgia', 9, 'bold italic'), fg='#7A8BA0', bg='#132240'
        )
        self.lbl_front_top.place(x=W//2, y=42, anchor='center')

        self.lbl_hand = tk.Label(
            self.canvas, text='',
            font=('Georgia', 52, 'bold'), fg='#FFFFFF', bg='#132240'
        )
        self.lbl_hand.place(x=W//2, y=128, anchor='center')

        self.lbl_hand_sub = tk.Label(
            self.canvas, text='',
            font=('Georgia', 13, 'italic'), fg='#C9A84C', bg='#132240'
        )
        self.lbl_hand_sub.place(x=W//2, y=198, anchor='center')

        # Back: dealer + action labels (hidden initially)
        self.lbl_dealer_top = tk.Label(
            self.canvas, text="DEALER'S UP CARD",
            font=('Georgia', 9, 'bold italic'), fg='#7A8BA0', bg='#132240'
        )

        self.lbl_dealer_card = tk.Label(
            self.canvas, text='',
            font=('Georgia', 40, 'bold'), fg='#FFFFFF', bg='#132240'
        )

        self.lbl_action_lbl = tk.Label(
            self.canvas, text='ACTION',
            font=('Georgia', 9, 'bold italic'), fg='#7A8BA0', bg='#132240'
        )

        self.lbl_action = tk.Label(
            self.canvas, text='',
            font=('Georgia', 30, 'bold'), fg='#FFFFFF', bg='#132240',
            width=14, relief='flat'
        )

        # Dealer card pip corners (decorative)
        self.pip_tl = tk.Label(self.canvas, text='', font=('Georgia', 14, 'bold'),
                               fg='#C9A84C', bg='#132240')
        self.pip_br = tk.Label(self.canvas, text='', font=('Georgia', 14, 'bold'),
                               fg='#C9A84C', bg='#132240')

        # ── Button row ───────────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg='#0A1628')
        btn_frame.pack(pady=(0, PAD))

        btn_cfg = dict(
            font=('Georgia', 11, 'bold'),
            relief='flat', cursor='hand2',
            padx=18, pady=8, bd=0
        )

        self.flip_btn = tk.Button(
            btn_frame, text='FLIP  ▶', bg='#C9A84C', fg='#0A1628',
            activebackground='#E2C060', activeforeground='#0A1628',
            command=self._flip, **btn_cfg
        )
        self.flip_btn.grid(row=0, column=0, padx=8)

        self.next_btn = tk.Button(
            btn_frame, text='NEXT  ›', bg='#1E3A5F', fg='#C9A84C',
            activebackground='#254d7f', activeforeground='#E2C060',
            command=self._next, state='disabled', **btn_cfg
        )
        self.next_btn.grid(row=0, column=1, padx=8)

        self.shuffle_btn = tk.Button(
            btn_frame, text='⇌  SHUFFLE', bg='#1E3A5F', fg='#C9A84C',
            activebackground='#254d7f', activeforeground='#E2C060',
            command=self._shuffle, **btn_cfg
        )
        self.shuffle_btn.grid(row=0, column=2, padx=8)

        # ── Legend ───────────────────────────────────────────────
        leg_frame = tk.Frame(self.root, bg='#0A1628')
        leg_frame.pack(pady=(0, 12))

        for action, color in ACTION_COLORS.items():
            lf = tk.Frame(leg_frame, bg=color, padx=6, pady=2)
            lf.pack(side='left', padx=4)
            tk.Label(lf, text=f'{ACTION_SHORT[action]} = {action}',
                     font=('Courier', 8, 'bold'),
                     fg='white' if action != 'Hit' else '#1a1a1a',
                     bg=color).pack()

        # ── Disclaimer ───────────────────────────────────────────
        disc_frame = tk.Frame(self.root, bg='#0A1628')
        disc_frame.pack(pady=(0, PAD), padx=PAD)

        tk.Label(
            disc_frame,
            text='DISCLAIMER: Blackjack, as is all gambling, is a game of chance. This strategy does not guarantee success. Gambling addiction? Call 1-800-GAMBLER',
            font=('Courier', 7),
            fg='#7A8BA0',
            bg='#0A1628',
            wraplength=560,
            justify='center'
        ).pack()

        tk.Label(
            disc_frame,
            text='This app was developed by Taylor Gibson as a practice development for using Claude Code.',
            font=('Courier', 6),
            fg='#5A6B80',
            bg='#0A1628',
            wraplength=560,
            justify='center'
        ).pack(pady=(4, 0))

    def _draw_card_bg(self):
        """Draw the card background with rounded corners and texture."""
        W, H = 560, 260
        r = 18
        pts = [r, 0, W-r, 0, W, r, W, H-r, W-r, H, r, H, 0, H-r, 0, r]
        self.canvas.create_polygon(pts, smooth=True, fill='#132240',
                                   outline='#2A4070', width=2)
        # felt texture lines (subtle)
        for y in range(0, H, 22):
            self.canvas.create_line(0, y, W, y, fill='#162848', width=1)

    # ── Card Logic ───────────────────────────────────────────────
    def _show_card(self):
        """Display the current flashcard (front side)."""
        if self.index >= len(self.cards):
            self._end_of_deck()
            return

        card = self.cards[self.index]
        self.flipped = False

        # Section label
        section = self._section(card['hand'])
        self.lbl_hand_sub.config(text=section)
        self.lbl_hand.config(text=card['hand'], fg='#FFFFFF')
        self.lbl_front_top.config(text='YOUR HAND')

        # Hide back labels
        for w in (self.lbl_dealer_top, self.lbl_dealer_card,
                  self.lbl_action_lbl, self.lbl_action,
                  self.pip_tl, self.pip_br):
            w.place_forget()

        # Show front labels
        self.lbl_front_top.place(x=280, y=42, anchor='center')
        self.lbl_hand.place(x=280, y=128, anchor='center')
        self.lbl_hand_sub.place(x=280, y=198, anchor='center')

        # Buttons
        self.flip_btn.config(state='normal', text='FLIP  ▶')
        self.next_btn.config(state='disabled')

        # Progress
        total = len(self.cards)
        self.progress_lbl.config(text=f'Card {self.index+1} of {total}')
        c, w = self.score['correct'], self.score['wrong']
        self.score_lbl.config(
            text=f'✓ {c}   ✗ {w}' if (c+w) else ''
        )

    def _flip(self):
        """Flip the card to show the strategy table."""
        if self.flipped:
            return
        self.flipped = True
        card = self.cards[self.index]
        player_hand = card['hand']

        # Hide front
        self.lbl_front_top.place_forget()
        self.lbl_hand.place_forget()
        self.lbl_hand_sub.place_forget()

        # Clear canvas and draw the strategy table
        self.canvas.delete('table_items')
        self._draw_strategy_table(player_hand)

        self.flip_btn.config(state='disabled', text='FLIPPED')
        self.next_btn.config(state='normal')
        self.score['seen'] += 1

    def _draw_strategy_table(self, player_hand):
        """Display the full strategy table for the given player hand."""
        # Dealer cards (columns)
        dealer_cards = DEALER_CARDS
        
        # Get actions for this hand against all dealer cards
        actions = []
        for dealer in dealer_cards:
            action = STRATEGY.get((player_hand, dealer), 'N/A')
            actions.append(action)
        
        # Draw header
        self.canvas.create_text(
            280, 22, text=f'Player Hand: {player_hand}',
            font=('Georgia', 12, 'bold'), fill='#C9A84C',
            tags='table_items'
        )
        
        # Draw the table with dealer cards and actions
        start_y = 50
        row_height = 22
        col_width = 48
        
        # Dealer card row
        self.canvas.create_text(
            30, start_y, text='Dealer:',
            font=('Georgia', 9, 'bold'), fill='#7A8BA0',
            anchor='w', tags='table_items'
        )
        
        for i, dealer in enumerate(dealer_cards):
            x = 100 + i * col_width
            self.canvas.create_text(
                x, start_y, text=dealer,
                font=('Georgia', 9, 'bold'), fill='#C9A84C',
                tags='table_items'
            )
        
        # Action row
        self.canvas.create_text(
            30, start_y + row_height, text='Action:',
            font=('Georgia', 9, 'bold'), fill='#7A8BA0',
            anchor='w', tags='table_items'
        )
        
        for i, action in enumerate(actions):
            x = 100 + i * col_width
            y = start_y + row_height
            short_action = ACTION_SHORT.get(action, action)
            color = ACTION_COLORS.get(action, '#555555')
            text_color = 'white' if action != 'Hit' else '#1a1a1a'
            
            # Draw colored background box
            box_width = 36
            box_height = 18
            self.canvas.create_rectangle(
                x - box_width // 2, y - 9,
                x + box_width // 2, y + 9,
                fill=color, outline='#2A4070', width=1,
                tags='table_items'
            )
            
            self.canvas.create_text(
                x, y, text=short_action,
                font=('Georgia', 8, 'bold'), fill=text_color,
                tags='table_items'
            )

    def _next(self):
        """Move to the next flashcard."""
        self.canvas.delete('divider')
        self.canvas.delete('table_items')
        self.index += 1
        self._show_card()

    def _shuffle(self):
        """Shuffle the cards and restart."""
        self.canvas.delete('divider')
        self.canvas.delete('table_items')
        random.shuffle(self.cards)
        self.index = 0
        self.score = {'correct': 0, 'wrong': 0, 'seen': 0}
        self._show_card()

    def _end_of_deck(self):
        """Display end-of-deck message."""
        for w in (self.lbl_front_top, self.lbl_hand, self.lbl_hand_sub,
                  self.lbl_dealer_top, self.lbl_dealer_card,
                  self.lbl_action_lbl, self.lbl_action,
                  self.pip_tl, self.pip_br):
            w.place_forget()
        self.canvas.delete('divider')
        self.canvas.delete('table_items')
        self.canvas.create_text(
            280, 130, text='🃏  Deck Complete!\nPress SHUFFLE to restart.',
            font=('Georgia', 18, 'bold'), fill='#C9A84C',
            justify='center', tags='done'
        )
        self.flip_btn.config(state='disabled')
        self.next_btn.config(state='disabled')
        self.progress_lbl.config(text='All cards reviewed!')

    @staticmethod
    def _section(hand):
        """Determine which section a hand belongs to (Hard, Soft, or Pairs)."""
        pairs    = {'A,A / 8,8','10,10','9,9','7,7','6,6','5,5','4,4','3,3','2,2'}
        soft     = {'A,9 / A,10','A,8','A,7','A,6','A,5','A,4','A,3','A,2'}
        if hand in pairs:  return 'PAIRS'
        if hand in soft:   return 'SOFT TOTAL'
        return 'HARD TOTAL'
