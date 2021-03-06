import os
import pwd

from .database import queries


def get_current_context(session=None):
    """
    Return a tuple, (srcf.database.Member, bool), for:
    - the current user
    - whether they're acting in sysadmin capacity (-adm)

    session may be a srcf.database.Session, if you have one.
    """
    try:
        pw_name = pwd.getpwuid(os.getuid()).pw_name
    except KeyError:
        pw_name = None

    attempts = {
        pw_name,
        os.environ.get("SUDO_USER"),
        os.environ.get("LOGNAME")
    } - {None, 'root'}

    if len(attempts) == 0:
        raise EnvironmentError("Unable to detect CRSID")
    elif len(attempts) != 1:
        raise EnvironmentError("Multiple CRSIDS? {0}"
                               .format(', '.join(attempts)))

    crsid = list(attempts)[0]
    admin = False
    if crsid.endswith("-adm"):
        crsid = crsid[:-4]
        admin = True

    return queries.get_user(crsid, session=session), admin


def get_current_user(session=None):
    """
    Return a srcf.database.Member for the current user.

    session may be a srcf.database.Session, if you have one.
    """
    user, _ = get_current_context(session)
    return user
