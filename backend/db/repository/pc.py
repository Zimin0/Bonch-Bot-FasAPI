import os
import aiofiles
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import UploadFile

from schemas.pc import PCCreate, PCGet, PCUpdate
from core.config import project_settings

