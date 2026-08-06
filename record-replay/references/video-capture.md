## Video Capture Guidance

* The `--video` flag records the entire screen during the active recording session.
* Output is an MP4 placed at `~/.hermes/recordings/<WORKFLOW_NAME>.mp4`.
* The video is automatically timestamped and matches the trace events, so you can scrub to see exactly what UI element was interacted with at any moment.
* Do **not** record sensitive screens (password entry, API keys, private chats). Stop the recording before such screens appear, or use a masked window.
* To share the video, upload it manually to a secure location; Hermes never uploads it automatically.
* The video can be replayed with standard media players; it does not affect the deterministic replay of the CUA trace.
