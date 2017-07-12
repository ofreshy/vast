

import attr

from vast.models import vast_v2
from vast.models.shared import check_and_convert
from vast.models.shared import ClassChecker


@attr.s()
class Icon(object):
    """
    program: Identifies the industry initiative that the icon supports. When icon elements of multiple
    programs are served in a chain of Wrapper ads, the video player uses this information to display only
    one icon from each program.
    • height: The height (in pixels) of the icon to be overlaid on the Ad.
    • width: The width (in pixels) of the icon to be overlaid on the Ad.
    • xPosition: The horizontal alignment location (in pixels) that the video player uses to place the top-left
    corner of the icon relative to the ad display area (not necessarily the video player display area).
    Accepted values are “left,” “right,” or a numeric value (in pixels). A value of “0” (zero) is the
    leftmost point of the ad display area.
    • yPosition: The vertical alignment location (in pixels) that the video player uses to place the top-left
    corner of the icon relative to the ad display area (not necessarily the video player display area).
    Accepted values are “top,” “bottom,” or a numeric value (in pixels). A value of “0” (zero) is the
    topmost point of the ad display area.
    """

    program = attr.ib()
    height = attr.ib()
    width = attr.ib()
    x_position = attr.ib()
    y_position = attr.ib()


@attr.s(frozen=True)
class Linear(object):
    """
    The most common type of video advertisement trafficked in the industry is a “linear ad”,
    which is an ad  that displays in the same area as the content but not at the same time as the content.
    In fact, the video  player must interrupt the content before displaying a linear ad.
    Linear ads are often displayed right  before the video content plays.
    This ad position is called a “predroll” position.
    For this reason, a linear ad  is often called a “predroll.”

    A <Linear> element has two required child elements, the <Duration> and the <MediaFiles>  element.
    Additionally three optional child elements are offered:
    <VideoClicks>, <AdParameters> and <TrackingEvents>.
    """
    REQUIRED = ("_linear_v2", )
    CLASSES = (
        ClassChecker("_linear_v2", vast_v2.Linear, False),
        ClassChecker("tracking_events", TrackingEvent, True),
        ClassChecker("icons", Icon, True),
    )

    _linear_v2 = attr.ib()
    tracking_events = attr.ib()
    icons = attr.ib()

    @classmethod
    def make(cls, duration, media_files, video_clicks=None, ad_parameters=None, tracking_events=None, icons=None):
        instance = check_and_convert(
            cls,
            args_dict=dict(
                _linear_v2=vast_v2.Linear.make(
                    duration,
                    media_files,
                    video_clicks=video_clicks,
                    ad_parameters=ad_parameters,
                ),
                tracking_events=tracking_events,
                icons=icons,
            ),
        )
        return instance

    @property
    def duration(self):
        return self._linear_v2.duration

    @property
    def media_files(self):
        return self._linear_v2.media_files

    @property
    def video_clicks(self):
        return self._linear_v2.video_clicks

    @property
    def ad_parameters(self):
        return self._linear_v2.ad_parameters


@attr.s()
class Ad(object):
    pass


@attr.s()
class Vast(object):
    pass


