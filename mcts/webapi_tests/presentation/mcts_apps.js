/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

'use strict';

var MCTSApps = {

  normalizeName: function(name) {
    return name.replace(/[- ]+/g, '').toLowerCase();
  },

  getRunningAppOrigin: function(name) {
    let manager = window.wrappedJSObject.AppWindowManager || window.wrappedJSObject.WindowManager;
    let runningApps = manager.getRunningApps();
    let origin;

    for (let property in runningApps) {
      if (runningApps[property].name == name) {
        origin = property;
      }
    }

    return origin;
  },

  locateWithName: function(name, aCallback) {
    var callback = aCallback || marionetteScriptFinished;
    function sendResponse(app, appName, entryPoint) {
      if (callback === marionetteScriptFinished) {
        if (typeof(app) === 'object') {
          var result = {
            name: app.manifest.name,
            origin: app.origin,
            entryPoint: entryPoint || null,
            normalizedName: appName
          };
          callback(result);
        } else {
          callback(false);
        }
      } else {
        callback(app, appName, entryPoint);
      }
    }

    let apps = window.wrappedJSObject.Applications.installedApps;
    let normalizedSearchName = MCTSApps.normalizeName(name);

    for (let manifestURL in apps) {
      let app = apps[manifestURL];
      let origin = null;
      let entryPoints = app.manifest.entry_points;
      if (entryPoints) {
        for (let ep in entryPoints) {
          let currentEntryPoint = entryPoints[ep];
          let appName = currentEntryPoint.name;

          if (normalizedSearchName === MCTSApps.normalizeName(appName)) {
            return sendResponse(app, appName, ep);
          }
        }
      } else {
        let appName = app.manifest.name;

        if (normalizedSearchName === MCTSApps.normalizeName(appName)) {
          return sendResponse(app, appName);
        }
      }
    }
    callback(false);
  },

  // Launches app with the specified name (e.g., 'Calculator'); returns the
  // app frame's id if successful, false if the app can't be found, or times
  // out if the app frame can't be found after launching the app.
  launchWithName: function(name) {
    MCTSApps.locateWithName(name, function(app, appName, entryPoint) {
      if (app) {
        let manager = window.wrappedJSObject.AppWindowManager || window.wrappedJSObject.WindowManager;
        let runningApps = manager.getRunningApps();
        let origin = MCTSApps.getRunningAppOrigin(appName);

        let sendResponse = function() {
          let app = runningApps[origin];
          let result = {
            frame: (app.browser) ? app.browser.element : app.frame.firstChild,
            src: (app.browser) ? app.browser.element.src : app.iframe.src,
            name: app.name,
            origin: origin
          };
          marionetteScriptFinished(result);
        };

        if (manager.getDisplayedApp() == origin) {
          console.log("app with origin '" + origin + "' is already running");
          sendResponse();
        }
        else {
          let appOpened = function() {
            window.removeEventListener('apploadtime', appOpened);
            window.removeEventListener('appopened', appOpened);
            waitFor(
              function() {
                console.log("app with origin '" + origin + "' has launched");
                sendResponse();
              },
              function() {
                origin = MCTSApps.getRunningAppOrigin(appName);
                return manager.getDisplayedApp() == origin;
              }
            );
          }
          window.addEventListener('apploadtime', appOpened);
          window.addEventListener('appopened', appOpened);
          console.log("launching app with name '" + appName + "'");
          app.launch(entryPoint || null);
        }
      } else {
        marionetteScriptFinished(false);
      }
    });
  }
};

