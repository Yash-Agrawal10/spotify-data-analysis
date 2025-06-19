from pydantic import BaseModel, HttpUrl, Field, model_validator
from typing import List, Dict, Literal, Any

class Image(BaseModel):
    url: HttpUrl
    height: int
    width: int

class Artist(BaseModel):
    id: str
    name: str
    genres: List[str]
    followers: int = Field(..., ge=0)
    popularity: int = Field(..., ge=0, le=100)
    images: List[Image]
    href: HttpUrl

    @model_validator(mode="before")
    @classmethod
    def pull_followers(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        raw = data.get("followers")
        if isinstance(raw, dict):
            if not isinstance(raw["total"], int):
                raise ValueError(f"Invalid followers.total: {raw["total"]!r}")
            data["followers"] = raw["total"]
        return data

class SimplifiedArtist(BaseModel):
    id: str
    name: str
    href: HttpUrl

class Album(BaseModel):
    id: str
    name: str
    album_type: Literal["album", "single", "compilation"]
    total_tracks: int = Field(..., ge=0)
    release_date: str
    release_date_precision: Literal["year", "month", "day"]
    artists: List[SimplifiedArtist]
    label: str
    popularity: int = Field(..., ge=0, le=100)
    images: List[Image]
    href: HttpUrl

class Track(BaseModel):
    id: str
    name: str
    album: Album
    artists: List[SimplifiedArtist]
    duration_ms: int = Field(..., ge=0)
    popularity: int = Field(..., ge=0, le=100)
    href: HttpUrl