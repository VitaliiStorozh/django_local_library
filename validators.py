from django.core.exceptions import ValidationError
from re import match


def validate_password(password: str):
    if not match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{6,}$", password):
        raise ValidationError(
            "Password must contain uppercase, lowercase, numeric, special symbols and length 6+ symbols")
    else:
        return password


def validate_names(data: str):
    if not (data[0].isupper() and data.isalpha()):
        raise ValidationError("All symbols must be letters and first one must be uppercase")
    else:
        return data
