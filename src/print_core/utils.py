"""
Utility helpers for print-core.
"""

from __future__ import annotations

import stat
from dataclasses import dataclass
from typing import Iterable, List, Optional

import ftputil.error
import ftputil.stat


@dataclass(frozen=True)
class UnixLsEntry:
    """
    A normalized representation of a single unix `ls -l` listing line.

    The fields reflect the most common pieces of data that `ls -l` style
    listings expose. Any fields not provided by the parser are left as None.
    """

    raw: str
    permissions: Optional[str] = None
    links: Optional[int] = None
    owner: Optional[str] = None
    group: Optional[str] = None
    size: Optional[int] = None
    mtime: Optional[float] = None
    month: Optional[str] = None
    day: Optional[str] = None
    time_or_year: Optional[str] = None
    name: Optional[str] = None


def _get_ftputil_unix_parser() -> ftputil.stat.UnixParser:
    """
    Return the ftputil Unix listing parser.
    """
    return ftputil.stat.UnixParser()


def parse_unixls_listings(
    lines: Iterable[str],
    *,
    parser: Optional[ftputil.stat.Parser] = None,
) -> List[UnixLsEntry]:
    """
    Parse a list of unix `ls -l` style listing lines using ftputil.

    Parameters
    ----------
    lines:
        Iterable of raw listing lines, e.g.
        "-rw-rw-rw-   1 root  root    539260 Nov 05 16:13 0_plate_1.gcode"

    parser:
        Optional ftputil parser. If omitted, this function uses the default
        Unix parser.

    Returns
    -------
    List[UnixLsEntry]
        Normalized entries with fields populated when available.
    """
    if parser is None:
        parser = _get_ftputil_unix_parser()

    entries: List[UnixLsEntry] = []
    for raw in lines:
        if parser.ignores_line(raw):
            continue
        try:
            parsed = parser.parse_line(raw)
        except ftputil.error.ParserError:
            continue

        permissions = (
            stat.filemode(parsed.st_mode) if parsed.st_mode is not None else None
        )
        entries.append(
            UnixLsEntry(
                raw=raw,
                permissions=permissions,
                links=parsed.st_nlink,
                owner=parsed.st_uid,
                group=parsed.st_gid,
                size=parsed.st_size,
                mtime=parsed.st_mtime,
                name=getattr(parsed, "_st_name", None),
            )
        )

    return entries
