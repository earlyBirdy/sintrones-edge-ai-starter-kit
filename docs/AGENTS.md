# AI Agents Add-on

This package adds three agents:
1) **System Recovery Agent** — watches MQTT heartbeats and triggers recovery actions.
2) **Adapter Auto-Gen Agent** — inspects MQTT/OPC UA and writes adapter config snippets.
3) **Release Agent** — runs `tools/healthcheck.py` and drafts release notes.

## Install
```bash
python -m pip install paho-mqtt pyyaml opcua requests
```

## Run
System recovery:
```bash
python -m src.agents.system_recovery_agent --config agents/system_recovery.yaml
```

Adapter autogen:
```bash
python -m src.agents.adapter_autogen_agent --mode mqtt --host localhost --topic factory/# --samples 30 --timeout 20
# or OPC UA
python -m src.agents.adapter_autogen_agent --mode opcua --endpoint opc.tcp://192.168.10.20:4840
```

Release agent:
```bash
python -m src.agents.release_agent --tag v0.3.0 --notes "Adapters + Vision QA"
```
Output files are written to `dist/`.
