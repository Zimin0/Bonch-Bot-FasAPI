from schemas.session import SessionCreate
from db.models.time_period import TimePeriod

class ValidationResult:
    def __init__(self, is_valid: bool, result_message: str = None):
        self.is_valid = is_valid
        self.result_message = result_message
        if self.result_message is None:
            if self.is_valid:
                self.result_message = "OK"
            else:
                self.result_message = "ERROR"
    
    def to_dict(self) -> str:
        return {"is_valid": self.is_valid, "result_message": self.result_message}
    
    @staticmethod
    def parse_only_errors(results: list["ValidationResult"]) -> list[str]:
        errors = []
        for res in results:
            if not res.is_valid:
                errors.append(res.result_message)
        return errors


class SessionValidator:
    """ Валидирует сессиию по бизнес правилам. """

    def __init__(self, MAX_SESSION_LENGTH: int = 60*60) -> None:
        self.MAX_SESSION_LENGTH = MAX_SESSION_LENGTH # в секундах
        
    def length_session_rule(self, session: SessionCreate):
        RULE = f"Длина сессии должна быть не более {self.MAX_SESSION_LENGTH // 60} минут. "
        length = TimePeriod.count_session_length(session.time_start, session.time_end)
        if length > self.MAX_SESSION_LENGTH:
            return ValidationResult(False, RULE)
        return ValidationResult(True)
    
    def free_time_check_rule(self, session_time_periods: list[TimePeriod]):
        RULE = "Это время уже занято."
        for tp in session_time_periods:
            if not tp.is_free:
                return ValidationResult(False, RULE)
        return ValidationResult(True)
    
    def start_before_end_rule(self, session: SessionCreate):
        RULE = "Время начала сессии должно быть ДО времени конца сесиии."
        if session.time_start >= session.time_end:
            return ValidationResult(False, RULE)
        return ValidationResult(True)

    def validate(self, session: SessionCreate, session_time_periods: list[TimePeriod]):
        """ Валидирует сессию. """
        results = []

        results.append(self.free_time_check_rule(session_time_periods))
        results.append(self.length_session_rule(session))
        results.append(self.start_before_end_rule(session))

        return ValidationResult.parse_only_errors(results)

