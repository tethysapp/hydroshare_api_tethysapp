from tethys_sdk.base import TethysAppBase, url_map_maker


class HydrosharePython(TethysAppBase):
    """
    Tethys app class for Hydroshare library.
    """

    name = 'Hydroshare library'
    index = 'hydroshare_python:home'
    icon = 'hydroshare_python/images/icon.gif'
    package = 'hydroshare_python'
    root_url = 'hydroshare-python'
    color = '#A9A9A9'
    description = '"An app which has the basic functions of the Hydroshare python client library"'
    tags = 'Python library, Hydroshare'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='hydroshare-python',
                controller='hydroshare_python.controllers.home'
            ),
        )

        return url_maps