import os
from datetime import datetime, timedelta, timezone

import boto3
from flask import Flask, jsonify

app = Flask(__name__)

REGION = os.getenv("AWS_REGION", "eu-north-1")
INSTANCE_ID = os.getenv("INSTANCE_ID", "i-082b5a3e5235cf8c4")

cloudwatch = boto3.client("cloudwatch", region_name=REGION)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/metrics")
def metrics():
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=3)

    queries = [
        {
            "Id": "cpu",
            "MetricStat": {
                "Metric": {
                    "Namespace": "AWS/EC2",
                    "MetricName": "CPUUtilization",
                    "Dimensions": [
                        {"Name": "InstanceId", "Value": INSTANCE_ID}
                    ],
                },
                "Period": 300,
                "Stat": "Average",
            },
            "ReturnData": True,
        },
        {
            "Id": "memory",
            "MetricStat": {
                "Metric": {
                    "Namespace": "CWAgent",
                    "MetricName": "mem_used_percent",
                    "Dimensions": [
                        {"Name": "InstanceId", "Value": INSTANCE_ID}
                    ],
                },
                "Period": 300,
                "Stat": "Average",
            },
            "ReturnData": True,
        },
        {
            "Id": "disk",
            "MetricStat": {
                "Metric": {
                    "Namespace": "CWAgent",
                    "MetricName": "disk_used_percent",
                    "Dimensions": [
                        {"Name": "InstanceId", "Value": INSTANCE_ID},
                        {"Name": "path", "Value": "/"},
                        {"Name": "device", "Value": "nvme0n1p1"},
                        {"Name": "fstype", "Value": "xfs"},
                    ],
                },
                "Period": 300,
                "Stat": "Average",
            },
            "ReturnData": True,
        },
    ]

    try:
        response = cloudwatch.get_metric_data(
            MetricDataQueries=queries,
            StartTime=start,
            EndTime=end,
            ScanBy="TimestampDescending",
        )

        values = {}
        timestamps = []

        for result in response["MetricDataResults"]:
            points = list(zip(
                result.get("Timestamps", []),
                result.get("Values", []),
            ))
            latest = max(points, key=lambda point: point[0], default=None)
            values[result["Id"]] = round(latest[1], 2) if latest else None
            if latest:
                timestamps.append(latest[0])

        return jsonify({
            "region": REGION,
            "instance_id": INSTANCE_ID,
            "updated_at": max(timestamps).isoformat() if timestamps else None,
            "metrics": {
                "cpu_percent": values.get("cpu"),
                "memory_percent": values.get("memory"),
                "disk_percent": values.get("disk"),
            },
        })

    except Exception:
        app.logger.exception("CloudWatch query failed")
        return jsonify({"error": "Unable to retrieve CloudWatch metrics"}), 502
