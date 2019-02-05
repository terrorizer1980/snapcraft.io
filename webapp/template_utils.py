# Core
import hashlib
import os


# generator functions for templates
def generate_slug(path):
    """
    Generate a slug for each page
    """
    if path.endswith(
        (
            "/snaps",
            "/listing",
            "/release",
            "/metrics",
            "/settings",
            "/account/details",
        )
    ):
        return "account"

    if path == "/":
        return "home"

    if path.startswith("/build"):
        return "build"

    if path.startswith("/blog"):
        return "blog"

    if path.startswith("/iot"):
        return "iot"

    return "store"


# template filters
def contains(arr, contents):
    """
    Template helper for detecting if an array contains an item
    """

    return contents in arr


def join(arr, separator=""):
    """
    Template helper for joining array items into a string, using a separator
    """

    return separator.join(arr)


def static_url(filename):
    """
    Template function for generating URLs to static assets:
    Given the path for a static file, output a url path
    with a hex hash as a query string for versioning
    """

    filepath = os.path.join("static", filename)
    url = "/" + filepath

    if not os.path.isfile(filepath):
        print("Could not find static file: " + filepath)
        return url

    # Use MD5 as we care about speed a lot
    # and not security in this case
    file_hash = hashlib.md5()
    with open(filepath, "rb") as file_contents:
        for chunk in iter(lambda: file_contents.read(4096), b""):
            file_hash.update(chunk)

    return url + "?v=" + file_hash.hexdigest()[:7]


def format_number(number: int):
    """
    Template function that transforms a int into a string
    with a comma between every thousands
    """
    return "{:,}".format(number)


def display_name(display_name, username):
    """Tempalate function that returns the displayed name if the username
    is the same, or the dispayed name and the username if differents
    """
    if display_name.lower() == username.lower():
        return display_name
    else:
        return f"{display_name} ({username})"


def time_live_stream():
    """Temporary function
    returns: 0 if stream is before the time
    returns: 1 if stream is now
    returns: 2 uf stream is close
    """

    import datetime
    import pytz

    tz = pytz.timezone("Europe/London")
    now = datetime.datetime.now(tz)
    stream = datetime.datetime(year=2019, month=2, day=6, hour=20, tzinfo=tz)

    end_stream = datetime.datetime(
        year=2019, month=2, day=6, hour=22, tzinfo=tz
    )

    if now < stream:
        return 0
    elif end_stream < now:
        return 2
    else:
        return 1
