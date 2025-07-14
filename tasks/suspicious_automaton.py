class SuspiciousBehaviorAutomaton:
    """Automaton specialized to detect Cross-Site Request Forgery (CSRF).

    The automaton monitors the typical flow of a form protected by a CSRF token.
    If the sequence of events deviates from the expected pattern it will end in
    one of the suspicious states ``S3``, ``S4`` or ``S5``.
    """

    # Set of accepting states (indicating suspicious behavior)
    FINAL_STATES = {"S3", "S4", "S5"}

    # Risk levels for each event
    EVENT_RISK = {
        "page_load": "Bajo",
        "form_render": "Bajo",
        "submit_request": "Medio",
        "missing_token": "Alto",
        "invalid_token": "Muy Alto",
        "valid_token": "Bajo",
        "external_referrer": "Alto",
        "replay_attempt": "Alto",
        "sensitive_action": "Muy Alto",
        "request_end": "Bajo",
    }

    def __init__(self):
        # Current state starts at S0
        self.state = "S0"

        # Transition table: (current_state, event) -> (next_state, probability)
        self.transitions = {
            ("S0", "page_load"): ("S1", 1.00),
            ("S1", "form_render"): ("S2", 0.95),
            ("S1", "submit_request"): ("S3", 0.05),
            ("S2", "submit_request"): ("S2", 0.10),
            ("S2", "missing_token"): ("S4", 0.30),
            ("S2", "invalid_token"): ("S5", 0.20),
            ("S2", "valid_token"): ("S1", 0.80),
            ("S3", "external_referrer"): ("S5", 0.40),
            ("S3", "sensitive_action"): ("S5", 0.60),
            ("S3", "request_end"): ("S0", 0.10),
            ("S4", "replay_attempt"): ("S5", 0.50),
            ("S4", "valid_token"): ("S1", 0.50),
        }

        # From the absorbing state S5 any event keeps the automaton in S5
        for event in self.EVENT_RISK.keys():
            self.transitions[("S5", event)] = ("S5", 1.0)

    def reset(self):
        """Return the automaton to the initial state."""
        self.state = "S0"

    def process_event(self, event):
        """Process a single event and update the current state.

        Returns a tuple ``(next_state, probability)`` if the event is valid for
        the current state, otherwise ``(current_state, 0.0)``.
        """
        key = (self.state, event)
        if key not in self.transitions:
            return self.state, 0.0

        next_state, prob = self.transitions[key]
        self.state = next_state
        return next_state, prob

    def event_risk(self, event):
        """Return the risk level associated with a given event."""
        return self.EVENT_RISK.get(event)

    def run(self, events):
        """Run the automaton over an iterable of events.

        Parameters
        ----------
        events : iterable of str
            Sequence of events to feed into the automaton.

        Returns
        -------
        state : str
            Final state after processing all events.
        suspicious : bool
            ``True`` if the final state is one of the accepting states.
        """
        for event in events:
            self.process_event(event)
        return self.state, self.state in self.FINAL_STATES
