from vast.models import vast_v2


class VastModelMixin(object):
    def make_wrapper_ad(self, wrapper=None):
        wrapper = wrapper or self.make_wrapper()
        return vast_v2.make_ad(
            id="ad_wrapper_id",
            wrapper=wrapper,
        )

    def make_inline_ad(self, inline=None):
        inline = inline or self.make_inline()
        return vast_v2.make_ad(
            id="ad_inline_id",
            inline=inline,
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
        return vast_v2.make_wrapper(
            ad_system=ad_system,
            vast_ad_tag_uri=vast_ad_tag_uri,
            ad_title=ad_title,
            impression=impression,
            error=error,
            creatives=creatives,
        )
