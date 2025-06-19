from pydantic import BaseModel, HttpUrl, Field, model_validator
from typing import Literal

class Image(BaseModel):
    url: HttpUrl
    height: int
    width: int

class Artist(BaseModel):
    id: str
    name: str
    genres: list[str]
    followers: int = Field(..., ge=0)
    popularity: int = Field(..., ge=0, le=100)
    images: list[Image]
    href: HttpUrl

    @model_validator(mode="before")
    @classmethod
    def pull_followers(cls, data):
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
    artists: list[SimplifiedArtist]
    label: str
    popularity: int = Field(..., ge=0, le=100)
    images: list[Image]
    href: HttpUrl

class SimplifiedAlbum(BaseModel):
    id: str
    name: str
    album_type: Literal["album", "single", "compilation"]
    total_tracks: int = Field(..., ge=0)
    release_date: str
    release_date_precision: Literal["year", "month", "day"]
    artists: list[SimplifiedArtist]
    images: list[Image]
    href: HttpUrl

class Track(BaseModel):
    id: str
    name: str
    album: SimplifiedAlbum
    artists: list[SimplifiedArtist]
    duration_ms: int = Field(..., ge=0)
    popularity: int = Field(..., ge=0, le=100)
    href: HttpUrl

class SimplifiedPlaylist(BaseModel):
    id: str
    name: str
    descrption: str = ""
    public: bool
    collaborative: bool
    images: list[Image]
    href: HttpUrl
    # owner
    # tracks