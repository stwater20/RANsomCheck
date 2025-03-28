import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { message, Table, Badge } from "antd";
import { WarningOutlined } from "@ant-design/icons";

interface LogData {
  id: string;
  number: number;
  name: string;
  uploadTime: string;
  status: string;
  result: number;
}

const columns = [
  {
    title: <span style={{ color: "#1677ff" }}>No.</span>,
    dataIndex: "number",
    key: "number",
    width: "10%",
    sorter: (a: any, b: any) => a.number - b.number
  },
  {
    title: <span style={{ color: "#1677ff" }}>Name</span>,
    dataIndex: "name",
    key: "name",
    width: "30%",
    render: (text: string, record: any) => (
      <Link to={`/analysis/details?id=${record.id}`}>
        {text}
      </Link>
    ),
    sorter: (a: any, b: any) => a.name.localeCompare(b.name)
  },
  {
    title: <span style={{ color: "#1677ff" }}>Upload Time</span>,
    dataIndex: "uploadTime",
    key: "uploadTime",
    width: "20%",
    sorter: (a: any, b: any) => a.uploadTime.localeCompare(b.uploadTime)
  },
  {
    title: <span style={{ color: "#1677ff" }}>Status</span>,
    dataIndex: "status",
    key: "status",
    width: "20%",
    render: (text: string) => (
      <Badge
        status={
          text === "Analyzing" ? "processing" :
          text === "Completed" ? "success" :
          text === "Failed" ? "error" :
          "default"
        }
        text={ text }
      />
    ),
    filters: [
      { text: "Pending", value: "Pending" },
      { text: "Analyzing", value: "Analyzing" },
      { text: "Completed", value: "Completed" },
      { text: "Failed", value: "Failed" }
    ],
    onFilter: (value: any, record: any) => record.status === value,
    sorter: (a: any, b: any) => a.status.localeCompare(b.status)
  },
  {
    title: <span style={{ color: "#1677ff" }}>Result</span>,
    dataIndex: "result",
    key: "result",
    width: "20%",
    render: (text: number) => (
      <span>
        {text === 1 ? (
          <span style={{ color: "#ff4d4f", fontWeight: "bold" }}>
            <WarningOutlined style={{ color: "#ff4d4f", marginRight: "0.3rem" }} />
            Ransomware
          </span>
        ) : text === 0 ? (
          "No ransomware detected"
        ) : (
          ""
        )}
      </span>
    ),
    filters: [
      { text: "Ransomware", value: 1 },
      { text: "No ransomware detected", value: 0 }
    ],
    onFilter: (value: any, record: any) => record.result === value,
    sorter: (a: any, b: any) => a.result - b.result
  }
];

export default function Analysis() {
  const [dataSource, setDataSource] = useState<LogData[]>([]);

  const fetchLogs = async () => {
    const trackerIdList = JSON.parse(localStorage.getItem("trackerIdList") || "[]");
    
    try {
      const data: LogData[] = await Promise.all(
        trackerIdList.map(async (trackerId: string, index: number) => {
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

          return {
            id: trackerId,
            number: index + 1,
            name: result.file_name,
            uploadTime: result.upload_flow.start_time,
            status: status,
            result: Array.isArray(result.result) && result.result.length === 1 ? result.result[0] : result.result,
          };
        })
      );
      setDataSource(data);
    } catch (error) {
      message.error("Error fetching log data.");
    }
  };

  useEffect(() => {
    fetchLogs();

    const intervalId = setInterval(fetchLogs, 60000);

    return () => clearInterval(intervalId);
  }, []);

  return(
    <Table 
      pagination={{ pageSize: 10 }} 
      dataSource={dataSource} 
      columns={columns} 
      rowClassName={(record) => record.result === 1 ? "ransomware-row" : ""}/>
  );
}