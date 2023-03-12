import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")



def resolve_string(song_obj, string):
    string = string.replace('$album', slugify(song_obj.album))
    string = string.replace('$name', slugify(song_obj.title))
    string = string.replace('$artist', slugify(song_obj.artist))
    string = string.replace('$year', slugify(song_obj.year))
    return string
