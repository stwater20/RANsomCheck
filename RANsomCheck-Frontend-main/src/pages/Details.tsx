import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { message, Descriptions, Badge, Alert } from "antd";
import type { DescriptionsProps } from "antd";

interface LogData {
  id: string;
  name: string;
  status: string;
  result: number;
  sha256: string;
  uploadTime: string;
  analysisStart: string;
  analysisCompleted: string;
  apiCalls: string[];
}

export default function Details() {
  const [data, setData] = useState<LogData | null>(null);
  const location = useLocation();
  const trackerId = new URLSearchParams(location.search).get("id");

  useEffect(() => {
    const fetchLog = async () => {
      try {
        const response = await fetch(`/api/log/${trackerId}`);
        if (!response.ok) {
          throw new Error("Failed to fetch log data");
        }

        const result = await response.json();

        var status = result.current_status;
        if (status === "Uploaded" || status === "Upload completed" || status === "Cuckoo uploaded" || status === "Cuckoo monitor started") {
          status = "Pending";
        } else if (status === "Cuckoo analyzing" || status === "Cuckoo completed" || status === "Model uploaded" || status === "Model analyzing") {
          status = "Analyzing";
        }  

        const data: LogData = {
          id: trackerId || "",
          name: result.file_name,
          status: status,
          result: Array.isArray(result.result) && result.result.length === 1 ? result.result[0] : result.result,
          sha256: result.SHA256,
          uploadTime: result.upload_flow.start_time,
          analysisStart: result.cuckoo_flow.analysis_time,
          analysisCompleted: result.model_flow.end_time,
          apiCalls: result["API calls"] || [],
        };

        setData(data);

      } catch (error) {
        message.error("Error fetching log data.");
      }
    };

    if (trackerId) {
      fetchLog();

      const intervalId = setInterval(fetchLog, 60000);

      return () => clearInterval(intervalId);
    }
  }, [trackerId]);

  if (!data) {
    return (
      <div style={{ display: "flex", justifyContent: "center" }}>Data not found.</div>
    );
  }

  const items: DescriptionsProps["items"] = [
    {
      key: "name",
      label: "Name",
      children: data.name,
    },
    {
      key: "status",
      label: "Status",
      children: (
        <Badge
          status={
            data.status === "Analyzing" ? "processing" :
            data.status === "Completed" ? "success" :
            data.status === "Failed" ? "error" :
            "default"
          }
          text={ data.status }
        />
      ),
    },
    {
      key: "result",
      label: "Result",
      children: (
        data.result === 1 ? (
          <span style={{ color: "#ff4d4f", fontWeight: "bold" }}>
            Ransomware
          </span>
        ) : data.result === 0 ? "No ransomware detected" : ""
      ),
    },
    {
      key: "SHA256",
      label: "SHA256",
      span: 3,
      children: data.sha256,
    },
    {
      key: "uploadTime",
      label: "Upload Time",
      span: 3,
      children: data.uploadTime,
    },
    {
      key: "analysisStart",
      label: "Analysis Start",
      span: 3,
      children: data.analysisStart,
    },
    {
      key: "analysisCompleted",
      label: "Analysis Completed",
      span: 3,
      children: data.analysisCompleted,
    },
    {
      key: "apiCalls",
      label: "API Calls",
      labelStyle: { width: "15%" },
      span: 3,
      children: data.apiCalls.join(", "),
    }
  ];

  return (
    <>
      {data.result === 1 && (
        <Alert
          message={<span style={{ color: "#ff4d4f", fontWeight: "bold", fontSize: "1.3rem" }}>Danger</span>}
          description={<span style={{ fontWeight: "bold", fontSize: "1.2rem" }}>Ransomware Alert! Do not open this file!</span>}
          type="error"
          style={{ marginBottom: "1rem" }}
        />
      )}
      <Descriptions title="Analysis Details" bordered items={items} />
    </>
  );
}