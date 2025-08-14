class EmailIdTgAlreadyExistsError(Exception):
    def __init__(self, tg_id: int, email: str):
        error_mes = f"Email: {email} or Telegram Id: {tg_id} is already exists"
        self.email = email
        self.tg_id = tg_id
        self.error_mes = error_mes
        super().__init__(error_mes)
