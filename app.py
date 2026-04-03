from WasteVision.logger import logging
from WasteVision.exception import AppException
import sys

try:
    a=3/'d'

except Exception as e:
    raise AppException(e,sys)

