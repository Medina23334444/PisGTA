class SuspiciousBehaviorAutomaton:
    """Automaton that models suspicious behavior using deterministic transitions.

    The automaton is defined by the following components:
    - States ``S0``..``S11``.
    - Input symbols are the various system events (``login``, ``failed_login`` ...).
    - Transition probabilities are stored together with the deterministic next state.
    - Accepting states ``S6``..``S10`` indicate suspicious behavior.
    """

    # Set of accepting states
    FINAL_STATES = {"S6", "S7", "S8", "S9", "S10"}

    # Risk levels for each event
    EVENT_RISK = {
        "login": "Bajo",
        "failed_login": "Medio",
        "read_file": "Bajo",
        "write_file": "Medio",
        "access_admin": "Alto",
        "logout": "Bajo",
        "upload_script": "Alto",
        "delete_file": "Alto",
        "create_user": "Muy Alto",
        "change_config": "Muy Alto",
        "open_port": "Muy Alto",
        "download_data": "Alto",
        "execute_binary": "Alto",
        "scan_ports": "Muy Alto",
    }

    def __init__(self):
        # Current state starts at S0
        self.state = "S0"

        # Transition table: (current_state, event) -> (next_state, probability)
        self.transitions = {
            ("S0", "login"): ("S1", 0.95),
            ("S0", "failed_login"): ("S5", 0.85),
            ("S5", "failed_login"): ("S5", 0.65),
            ("S1", "read_file"): ("S2", 0.80),
            ("S1", "write_file"): ("S3", 0.70),
            ("S1", "upload_script"): ("S4", 0.30),
            ("S2", "upload_script"): ("S4", 0.30),
            ("S3", "upload_script"): ("S4", 0.30),
            ("S1", "execute_binary"): ("S6", 0.20),
            ("S4", "execute_binary"): ("S6", 0.20),
            ("S1", "access_admin"): ("S7", 0.15),
            ("S5", "access_admin"): ("S7", 0.10),
            ("S6", "access_admin"): ("S7", 0.15),
            ("S7", "create_user"): ("S8", 0.10),
            ("S8", "change_config"): ("S9", 0.05),
            ("S9", "open_port"): ("S10", 0.03),
            ("S1", "download_data"): ("S11", 0.40),
            ("S1", "logout"): ("S0", 0.90),
        }

    def reset(self):
        """Return the automaton to the initial state."""
        self.state = "S0"

    def process_event(self, event):
        """Process a single event and update the current state.

        Returns a tuple ``(next_state, probability)`` if the event is valid for the
        current state, otherwise ``(current_state, 0.0)``.
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
            ``True`` if the final state is one of the accepting (suspicious) states.
        """
        for event in events:
            self.process_event(event)
        return self.state, self.state in self.FINAL_STATES
