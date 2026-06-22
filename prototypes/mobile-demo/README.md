# GhostEye WiFi-Only Live v0.3 Demo

Static browser/mobile prototype for the GhostEye WiFi-only non-CSI backend.

## Run

```bash
cd ~/Desktop/Ghost-Eye/prototypes/mobile-demo
python3 -m http.server 5173
```

Open <http://localhost:5173>, enter the backend URL (default `http://localhost:8000`), and click **Connect**.

## Backend

From the repository:

```bash
cd ghost_eye/backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Demo procedure

1. Connect the backend MacBook to the authorized NetGear or TP-Link WiFi router.
2. Start the GhostEye backend.
3. Start this browser demo with `python3 -m http.server 5173`.
4. Connect the demo to the backend URL.
5. Run empty-room calibration while the room is clear.
6. Have a consenting test participant enter the room or a coarse zone.
7. Watch `/scan`, the signal quality panel, AI analysis, and radar zone map change.

## Limitations

WiFi-only non-CSI mode provides coarse probabilistic estimates only. It does not
provide validated through-wall object imaging, exact object detection, or exact
person location. Use only in authorized, controlled, consent-based environments.
