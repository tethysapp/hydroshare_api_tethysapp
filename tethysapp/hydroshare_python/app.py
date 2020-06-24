from tethys_sdk.base import TethysAppBase, url_map_maker


class HydrosharePython(TethysAppBase):
    """
    Tethys app class for Hydroshare library.
    """

    name = 'HydroShare Python API Demonstration'
    index = 'hydroshare_python:home'
    icon = 'hydroshare_python/images/icon.gif'
    package = 'hydroshare_python'
    root_url = 'hydroshare-python'
    color = '#B22222'
    description = 'This app is to demonstrate the functions of the HydroShare Python api (hs_restclient)'
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
            UrlMap(
                name='get_file',
                url='hydroshare-python/get_file',
                controller='hydroshare_python.controllers.get_file'
            ),
            UrlMap(
                name='add_file',
                url='hydroshare-python/add_file',
                controller='hydroshare_python.controllers.add_file'
            ),
            UrlMap(
                name='delete_resource',
                url='hydroshare-python/delete_resource',
                controller='hydroshare_python.controllers.delete_resource'
            ),
            UrlMap(
                name='delete_file',
                url='hydroshare-python/delete_file',
                controller='hydroshare_python.controllers.delete_file'
            ),
            UrlMap(
                name='viewer',
                url='hydroshare-python/viewer',
                controller='hydroshare_python.controllers.viewer'
            ),
            UrlMap(
                name='download_file',
                url='hydroshare-python/download_file',
                controller='hydroshare_python.controllers.download_file'
            ),
            UrlMap(
                name='mapview',
                url='hydroshare-python/mapview',
                controller='hydroshare_python.controllers.mapview'
            ),
            UrlMap(
                name='filev',
                url='hydroshare-python/filev',
                controller='hydroshare_python.controllers.filev'
            ),
            UrlMap(
                name='metadata',
                url='hydroshare-python/metadata',
                controller='hydroshare_python.controllers.metadata'
            ),
            
        )

        return url_maps