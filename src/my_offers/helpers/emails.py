import re


EMAIL_PATTERN: re.Pattern = re.compile(
    r'^[=_0-9a-z+~\'!$&*^`|#%/?{}-]'
    r'+(\.[=_0-9a-z+~\'!$&*^`|#%/?{}-]+)*@(([-0-9a-z_]+\.)+)([a-z0-9-]{2,20})$',
    re.IGNORECASE
)


def is_correct_email(email: str) -> bool:
    return bool(
        re.match(
            pattern=EMAIL_PATTERN,
            string=email,
        )
    )
