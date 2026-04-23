class ValidationResult:
    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []

    def add_error(self, error):
        self.is_valid = False
        self.errors.append(str(error))

    def add_warning(self, warning):
        self.warnings.append(str(warning))

    def summary(self):
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings
        }

    def print_summary(self):
        print("\n===== VALIDATION RESULT =====")
        print("Valid:", self.is_valid)

        if self.errors:
            print("Errors:")
            for err in self.errors:
                print("-", err)

        if self.warnings:
            print("Warnings:")
            for warn in self.warnings:
                print("-", warn)