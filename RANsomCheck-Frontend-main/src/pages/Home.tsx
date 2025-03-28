import { useState } from "react";
import { InboxOutlined } from "@ant-design/icons";
import type { UploadProps } from "antd";
import { message, Upload, Button, Modal } from "antd";

const { Dragger } = Upload;

const trackerIdList = JSON.parse(localStorage.getItem("trackerIdList") || "[]");

function pushTrackerId(trackerId: string): void {
  if (trackerId != null) {
    trackerIdList.push(trackerId);
    localStorage.setItem("trackerIdList", JSON.stringify(trackerIdList));
  }
}

export default function Home() {

  const [open, setOpen] = useState(false);
  const [modalTitle, setModalTitle] = useState("");

  const props: UploadProps = {
    name: "file",
    multiple: true,
    customRequest: async ({ file, onSuccess, onError }: any) => {
      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();

        if (response.ok) {
          onSuccess(result, file);
          pushTrackerId(result.tracker_id);
          setModalTitle(result.message);
          showModal();
        } else {
          onError(result.error || result.message);
          message.error(result.error || result.message);
        }
        
      } catch (error) {
        onError(error);
        message.error("System error occurred.");
      }
    }
  };

  const showModal = () => {
    setOpen(true);
  };

  const handleOk = () => {
    setOpen(false);
  };

  const handleCancel = () => {
    setOpen(false);
    window.location.href = "/analysis";
  };

  return (
    <div className="file-upload">
      <Dragger {...props}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">
          Click or drag the file you want to analyze to this area to upload.<br/>
          Notice: The uploaded files will be used for academic research.
        </p>
        <p className="ant-upload-hint">
          Accepted file types: Windows Portable Executable files
        </p>
      </Dragger>
      <Modal
        open={open}
        title={modalTitle}
        onOk={handleOk}
        onCancel={handleCancel}
        footer={[
          <Button type="primary" onClick={handleOk}>
            Yes
          </Button>,
          <Button onClick={handleCancel}>
            No
          </Button>
        ]}
      >
        <p>Do you want to upload another file?</p>
      </Modal>
    </div>
  );
}