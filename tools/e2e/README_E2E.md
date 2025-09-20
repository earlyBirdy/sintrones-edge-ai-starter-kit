# E2E Dummy Data & Probes

This bundle helps you test the Sintrones Edge AI dashboard end-to-end **without real devices**.

## Files
- **generate_dummy_data.py** — seeds `data/edge.db` with realistic rows
- **e2e_probe.py** — runs sanity queries the tabs expect to use and prints sample outputs

## How to use
1. Ensure your repo is unpacked at:
   - `/mnt/data/sintrones_edge_ai_kit_0920/sintrones-edge-ai-starter-kit-main`
2. Create a virtualenv and install requirements (from repo root):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   python -m pip install --upgrade pip wheel setuptools
   python -m pip install -r requirements.txt
   ```
3. Seed the DB:
   ```bash
   python /mnt/data/e2e_templates/generate_dummy_data.py
   ```
4. Verify E2E probes:
   ```bash
   python /mnt/data/e2e_templates/e2e_probe.py
   ```
5. Launch Streamlit from repo root:
   ```bash
   streamlit run app.py
   ```

## Notes
- The scripts create `data/edge.db` in the repo, matching the app’s default (`core/db.py`).
- If a tab shows empty state, run the probe and confirm the corresponding table has rows.
