import os

class MCTSApps():

    def __init__(self, marionette):
        self.marionette = marionette
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, "mcts_apps.js"))
        self.marionette.import_script(js)

    def launch(self, name, switch_to_frame=True, url=None, launch_timeout=None):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script("MCTSApps.launchWithName('%s')" % name, script_timeout=launch_timeout)
        assert result, "Failed to launch app with name '%s'" % name
        app = GaiaApp(frame=result.get('frame'),
                      src=result.get('src'),
                      name=result.get('name'),
                      origin=result.get('origin'))
        if app.frame_id is None:
            raise Exception("App failed to launch; there is no app frame")
        if switch_to_frame:
            self.switch_to_frame(app.frame_id, url)
        return app

class GaiaApp(object):

    def __init__(self, origin=None, name=None, frame=None, src=None, manifest_url=None, entry_point=None):
        self.frame = frame
        self.frame_id = frame
        self.src = src
        self.name = name
        self.origin = origin
        self.manifest_url = manifest_url
        self.entry_point = entry_point

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
