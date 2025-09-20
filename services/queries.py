TRACEABILITY_JOIN = """
SELECT
  sr.id              AS reading_id,
  sr.ts              AS reading_ts,
  sr.device_id,
  sr.sensor_type,
  sr.value,
  sr.unit,
  ie.model_name,
  ie.pred_label,
  ie.pred_score,
  qr.passed,
  qr.defect_code,
  an.severity        AS anomaly_severity,
  an.note            AS anomaly_note
FROM sensor_readings sr
LEFT JOIN inference_events ie ON ie.reading_id = sr.id
LEFT JOIN quality_results  qr ON qr.reading_id = sr.id
LEFT JOIN anomalies        an ON an.reading_id = sr.id
WHERE sr.ts >= datetime('now', ?)
  AND (? = '' OR sr.device_id = ?)
ORDER BY sr.ts DESC
LIMIT ? OFFSET ?;
"""
