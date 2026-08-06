# Granting macOS Screen Recording Permission

1. Open **System Settings** → **Privacy & Security** → **Screen Recording**.
2. Click the lock icon and authenticate.
3. Add the **Hermes** (or the `python` executable used by the Hermes CLI) to the list of allowed apps.
4. Confirm and close Settings.
5. Restart the Hermes gateway (`hermes gateway restart`) so the permission takes effect.

After this, `record-replay start <NAME> --video` will create an MP4 file in `~/.hermes/recordings/` without the `SCShareableContent` error.
