from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class User(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None

class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[Dict[str, Any]] = None
    inline_query: Optional[Dict[str, Any]] = None
    callback_query: Optional[Dict[str, Any]] = None
    chosen_inline_result: Optional[Dict[str, Any]] = None

class WhisperData(BaseModel):
    inline_message_id: str
    message: str
    sender_id: int
    recipient_ids: List[int]
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

class UserData(BaseModel):
    id: int
    target_user: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class InlineQueryData(BaseModel):
    id: str
    from_user: User
    query: str
    offset: str = ""

class CallbackQueryData(BaseModel):
    id: str
    from_user: User
    data: str
    inline_message_id: Optional[str] = None

class ChosenInlineResultData(BaseModel):
    result_id: str
    from_user: User
    query: str
    inline_message_id: Optional[str] = None