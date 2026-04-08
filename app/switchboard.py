from __future__ import annotations

from dataclasses import dataclass

from app.users import ForeignUser, LocalUser, User


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._cross_border_count: int = 0

    @staticmethod
    def _parse_user_id(user_id: str) -> int:
        user_id_result = user_id.strip()
        if not user_id_result.isdigit():
            raise ValueError("Invalid user id")
        return int(user_id_result)

    def _create_user(self, user_id: str, name: str, phone: str) -> User:
        user_id_int = self._parse_user_id(user_id)
        fullname = name.strip()
        phone_stripped = phone.strip()
        if phone_stripped.startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(id=user_id_int, fullname=fullname, phone=phone_stripped)
        return ForeignUser(id=user_id_int, fullname=fullname, phone=phone_stripped)

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,receiver_id,receiver_name,receiver_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        parts = raw_call.split(',')
        if len(parts) != 6:
            raise ValueError("Invalid raw call format")
        
        caller = self._create_user(parts[0], parts[1], parts[2])
        receiver = self._create_user(parts[3], parts[4], parts[5])
        
        active_call = ActiveCall(caller=caller, receiver=receiver)
        self._active_calls.append(active_call)
        
        if active_call.is_cross_border:
            self._cross_border_count += 1
            
        return active_call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_count
