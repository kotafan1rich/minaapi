class CreateReferralException(Exception):
    def __init__(self):
        super().__init__()


class UserAlreadyHasReferralsException(Exception):
    def __init__(self):
        super().__init__()
