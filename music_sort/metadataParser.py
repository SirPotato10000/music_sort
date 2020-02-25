from tinytag import TinyTag, TinyTagException
from os import path

from . import metadataHolder

DEFAULT_ATTRIBUTE_VALUE = "Unknown"
DEFAULT_BITRATE_VALUE = float(0.00)


def parseSongList(songList: list):
    parsedSongs = []
    for i, song in enumerate(songList):
        print("Parsing song " + str(i + 1) + " of " + str(len(songList)), end="\r")
        try:
            metadata = parseSong(song)
            parsedSongs.append(metadata)
        except (PermissionError, TinyTagException) as e:
            print(song)
            print(e)
    return tuple(parsedSongs)


def parseSong(songPath: str):
    songInfo = TinyTag.get(songPath)
    metadata = metadataHolder.MetadataHolder(
        songInfo.title,
        songInfo.album,
        songInfo.albumartist,
        songInfo.artist,
        songInfo.genre,
        songInfo.bitrate,
        songInfo.track,
        songInfo.year,
        songPath,
        path.basename(songPath),
        path.splitext(songPath)[1],
    )
    cleanMetadata(metadata)
    return metadata


def cleanMetadata(metadata):
    criticalProperties = [
        "title",
        "album",
        "albumartist",
        "artist",
        "genre",
        "track",
        "year",
    ]
    for property in criticalProperties:
        if type(getattr(metadata, property, DEFAULT_ATTRIBUTE_VALUE)) != str:
            setattr(metadata, property, DEFAULT_ATTRIBUTE_VALUE)
    if type(getattr(metadata, "bitrate", DEFAULT_ATTRIBUTE_VALUE)) != float:
        setattr(metadata, "bitrate", DEFAULT_BITRATE_VALUE)
