from vast.models import vast_v2


class VastModelMixin(object):
    def make_vast(self, version=u"2.0", ad=None):
        return vast_v2.Vast.make(
            version=version,
            ad=ad or self.make_wrapper_ad(),
        )
    def make_wrapper_ad(self, wrapper=None):
        return vast_v2.Ad.make_wrapper(
            id="ad_wrapper_id",
            wrapper=wrapper or self.make_wrapper(),
        )

    def make_inline_ad(self, inline=None):
        return vast_v2.Ad.make_inline(
            id="ad_inline_id",
            inline=inline or self.make_inline(),
        )

    @staticmethod
    def make_wrapper(
            ad_system=u"Mag",
            vast_ad_tag_uri=u"https://www.magu.com",
            ad_title=u"MagAd",
            impression=u"https://www.mag_impression.com",
            error=u"https://www.mag_error.com",
            creatives=None,
    ):
        return vast_v2.Wrapper.make(
            ad_system=ad_system,
            vast_ad_tag_uri=vast_ad_tag_uri,
            ad_title=ad_title,
            impression=impression,
            error=error,
            creatives=creatives,
        )

    def make_inline(
            self,
            ad_system=u"Mag",
            ad_title=u"MagAd",
            impression=u"https://www.mag_impression.com",
            creatives=None,
    ):
        return vast_v2.Inline.make(
            ad_system=ad_system,
            ad_title=ad_title,
            impression=impression,
            creatives=creatives or self.make_creatives()
        )

    def make_creatives(self):
        return [self.make_creative()]


    def make_creative(
            self,
            linear=None, non_linear=None, companion_ads=None,
            id="creative_id", sequence=None, ad_id="ad_id",
            api_framework=vast_v2.ApiFramework.VPAID,
    ):
        return vast_v2.Creative.make(
            linear=linear or self.make_linear_creative(),
            non_linear=non_linear,
            companion_ads=companion_ads,
            id=id,
            sequence=sequence,
            ad_id=ad_id,
            api_framework=api_framework,
        )

    @staticmethod
    def make_tracking_event(
            tracking_event_uri="https://http.mag.u",
            tracking_event_type="close",
    ):
        return vast_v2.TrackingEvent.make(
            tracking_event_uri=tracking_event_uri,
            tracking_event_type=tracking_event_type,
        )

    def make_linear_creative(
            self,
            duration=15,
            media_files=None,
    ):
        return vast_v2.Linear.make(
            duration,
            media_files=media_files or self.make_media_files(),
            video_clicks=None,
            ad_parameters=None,
            tracking_events=None
        )

    def make_media_files(self):
        return [
            self.make_media_file(),
        ]

    @staticmethod
    def make_media_file(
            asset=u"https://www.mag.u",
            delivery=u"progressive",
            type=u"video/mp4",
            width=300,
            height=250,
            bitrate=150,
            codec=None,
            id="media_file_1_id",
    ):
        return vast_v2.MediaFile.make(
            asset, delivery, type, width, height,
            codec, id, bitrate, min_bitrate=None, max_bitrate=None,
            scalable=None, maintain_aspect_ratio=None, api_framework=None
        )