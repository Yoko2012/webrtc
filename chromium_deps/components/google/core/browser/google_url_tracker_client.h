// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef COMPONENTS_GOOGLE_GOOGLE_URL_TRACKER_CLIENT_H_
#define COMPONENTS_GOOGLE_GOOGLE_URL_TRACKER_CLIENT_H_

#include "base/macros.h"

class GoogleURLTracker;

// Interface by which GoogleURLTracker communicates with its embedder.
class GoogleURLTrackerClient {
 public:
  GoogleURLTrackerClient();
  virtual ~GoogleURLTrackerClient();

  // Sets the GoogleURLTracker that is associated with this client.
  void set_google_url_tracker(GoogleURLTracker* google_url_tracker) {
    google_url_tracker_ = google_url_tracker;
  }

  // Enables or disables listening for navigation starts. OnNavigationPending
  // will be called for each navigation start if listening is enabled.
  virtual void SetListeningForNavigationStart(bool listen) = 0;

  // Returns whether or not the client is currently listening for navigation
  // starts.
  virtual bool IsListeningForNavigationStart() = 0;

 protected:
  GoogleURLTracker* google_url_tracker() { return google_url_tracker_; }

 private:
  GoogleURLTracker* google_url_tracker_;

  DISALLOW_COPY_AND_ASSIGN(GoogleURLTrackerClient);
};

#endif  // COMPONENTS_GOOGLE_GOOGLE_URL_TRACKER_CLIENT_H_
