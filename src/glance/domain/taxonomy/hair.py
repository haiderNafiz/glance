from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class HairLengthCategory(str, Enum):
    VERY_SHORT = "VERY_SHORT"           # Close to scalp (typically <= 3 cm)
    SHORT = "SHORT"                     # Above jaw/neck region
    MEDIUM = "MEDIUM"                   # Jaw/neck to shoulder
    SHOULDER_LENGTH = "SHOULDER_LENGTH" # Reaches shoulder level
    LONG = "LONG"                       # Below shoulder (upper/mid back)
    VERY_LONG = "VERY_LONG"             # Substantially below mid-back (waist level or below)
    UNKNOWN = "UNKNOWN"                 # Insufficient visual evidence

class LengthLandmark(str, Enum):
    SCALP_CLOSE = "SCALP_CLOSE"
    EAR = "EAR"
    JAW = "JAW"
    NECK = "NECK"
    SHOULDER = "SHOULDER"
    UPPER_BACK = "UPPER_BACK"
    MID_BACK = "MID_BACK"
    WAIST = "WAIST"
    BELOW_WAIST = "BELOW_WAIST"
    UNKNOWN = "UNKNOWN"

class HairLength(BaseModel):
    category: HairLengthCategory = HairLengthCategory.UNKNOWN
    landmark: LengthLandmark = LengthLandmark.UNKNOWN
    estimated_cm: Optional[float] = Field(default=None, ge=0.0, description="Optional length in centimeters")

class HairTexture(str, Enum):
    STRAIGHT = "STRAIGHT"
    WAVY = "WAVY"
    CURLY = "CURLY"
    COILY = "COILY"
    MIXED = "MIXED"
    UNKNOWN = "UNKNOWN"

class WavePattern(str, Enum):
    NONE = "NONE"
    LOOSE = "LOOSE"
    MODERATE = "MODERATE"
    DEFINED = "DEFINED"
    UNKNOWN = "UNKNOWN"

class ApparentVolume(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"

class ApparentDensity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"

class HairColorFamily(str, Enum):
    BLACK = "BLACK"
    DARK_BROWN = "DARK_BROWN"
    MEDIUM_BROWN = "MEDIUM_BROWN"
    LIGHT_BROWN = "LIGHT_BROWN"
    BLONDE = "BLONDE"
    RED = "RED"
    GRAY = "GRAY"
    FASHION_COLOR = "FASHION_COLOR"
    MULTI_COLOR = "MULTI_COLOR"
    UNKNOWN = "UNKNOWN"

class HighlightType(str, Enum):
    NONE = "NONE"
    SUBTLE = "SUBTLE"
    VISIBLE = "VISIBLE"
    STRONG = "STRONG"
    MULTI_TONE = "MULTI_TONE"
    UNKNOWN = "UNKNOWN"

class HaircutStructure(str, Enum):
    ONE_LENGTH = "ONE_LENGTH"
    BLUNT = "BLUNT"
    LAYERED = "LAYERED"
    TEXTURED = "TEXTURED"
    BOB = "BOB"
    LOB = "LOB"
    PIXIE = "PIXIE"
    SHAG = "SHAG"
    UNKNOWN = "UNKNOWN"
