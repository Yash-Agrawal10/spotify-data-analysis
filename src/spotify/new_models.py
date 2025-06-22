from pydantic import BaseModel, model_validator
from typing import Optional

class SpotifyArtist(BaseModel):
    id: str
    name: str

class SpotifyAlbum(BaseModel):
    id: str
    name: str
    isrc: str

class SpotifyTrack(BaseModel):
    id: str
    name: str
    isrc: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def extract_isrc(cls, data):
        ext = data.pop("external_ids", None)
        if isinstance(ext, dict) and "isrc" in ext:
            data["isrc"] = ext["isrc"]
        return data

class SpotifyPlaylist(BaseModel):
    id: str
    name: str
    tracks: Optional[list[SpotifyTrack]] = None
