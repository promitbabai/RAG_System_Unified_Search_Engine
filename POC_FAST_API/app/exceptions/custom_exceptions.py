class UserNotFoundException(Exception):
    """Raised when the requested user is not found."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"User not found for user_id={user_id}"
        super().__init__(self.message)
