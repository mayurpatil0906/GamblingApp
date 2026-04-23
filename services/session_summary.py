class SessionSummary:
    def display_session_summary(self, summary_data):
        if not summary_data:
            print("No session summary available.")
            return

        print("\n===== SESSION SUMMARY =====")
        for key, value in summary_data.items():
            print(f"{key}: {value}")