#!/usr/bin/env python

from contextlib import closing
import copy
import json
from StringIO import StringIO
from zipfile import ZipFile, ZIP_DEFLATED

import webapp2
from webapp2_extras import jinja2

from dummydata import generate_id, generate_name, generate_description
import constants


XSS = '<script>alert("ALL YOUR BASE ARE BELONG TO KRUPA")</script>'
MANIFEST = {
    "version": "1.0",
    "name": "Packaged App",
    "description": "This is a packaged app",
    "icons": {
        "16": "/icons/16.png",
        "32": "/icons/32.png",
        "256": "/icons/256.png"
    },
    "developer": {
        "name": "Mozilla Labs",
        "url": "http://mozillalabs.com"
    },
    "installs_allowed_from": [
        "https://marketplace.mozilla.org/",
        "https://marketplace-dev.mozilla.org/"
    ],
    "launch_path": "/index.html",
    "locales": {
        "es": {
            "name": "",
            "description": ""
        },
        "pt-br": {
            "name": "",
            "description": ""
        },
    },
    "default_locale": "en",
    "screen_size": {
        "min_width": "600",
        "min_height": "300"
    },
    "required_features": [
        "touch", "geolocation", "webgl"
    ],
    "orientation": "landscape",
    "fullscreen": "true"
}
def _get_manifest():
    return copy.deepcopy(MANIFEST)


class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template_raw(self, template, **context):
        return self.jinja2.render_template(template, **context)

    def render_template(self, template, **context):
        rv = self.render_template_raw(template, **context)
        self.response.write(rv)


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("main.html")


class BuildHandler(BaseHandler):
    def get(self):
        self._build()

    def post(self):
        self._build()

    def _add_file(self, f, name, path):
        with open(path, "r") as p:
            self._add(f, name, p.read())

    def _add(self, f, name, content):
        f.writestr(name, content)

    def _build(self):
        self.response.headers['Content-Type'] = "application/zip"
        self.response.headers['Content-Disposition'] = (
            'attachment; filename="%s.zip"' % generate_id())

        sio = StringIO()
        with ZipFile(file=sio, mode="w", compression=ZIP_DEFLATED) as outfile:
            manifest = _get_manifest()

            if not self.request.get("exclude_icons"):
                self._add_file(outfile, "icons/16.png", "content/icons/16.png")
                self._add_file(outfile, "icons/32.png", "content/icons/32.png")
                self._add_file(outfile, "icons/256.png",
                               "content/icons/256.png")
            else:
                manifest["icons"] = {}

            if self.request.get("opt_xss"):
                manifest["name"] = XSS
                manifest["description"] = XSS
                for locale, data in manifest["locales"].items():
                    data["name"] = XSS
                    data["description"] = XSS
            else:
                manifest["name"] = generate_name()
                manifest["description"] = generate_description()
                for locale, data in manifest["locales"].items():
                    data["name"] = generate_name()
                    data["description"] = generate_description()

            if not self.request.get("exclude_manifest"):
                self._add(outfile, "manifest.webapp", json.dumps(manifest))

            css = set()
            js = set()

            if not self.request.get("exclude_css"):
                self._add_file(outfile, "style.css", "content/style.css")
                css.add("style.css")
            if not self.request.get("exclude_js"):
                self._add_file(outfile, "script.js", "content/script.js")
                js.add("script.js")

            if self.request.get("include_bcss"):
                self._add_file(outfile, "broken_style.css",
                               "content/broken_style.css")
                css.add("broken_style.css")
            if self.request.get("include_bjs"):
                self._add_file(outfile, "broken_script.js",
                               "content/broken_script.js")
                js.add("broken_script.js")
            if self.request.get("include_jquery"):
                self._add_file(outfile, "jquery.js", "content/jquery.js")
                js.add("jquery.js")

            if not self.request.get("exclude_html"):
                manifest["css"] = css
                manifest["js"] = js
                self._add(outfile, "index.html",
                        self.render_template_raw("app_index.html", **manifest))

        sio.seek(0)
        self.response.out.write(sio.getvalue())


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/build', BuildHandler)],
                              debug=constants.DEBUG)
