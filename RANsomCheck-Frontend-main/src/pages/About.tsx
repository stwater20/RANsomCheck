import { Card, Avatar, Row, Col } from "antd";
import { BookOutlined, TeamOutlined } from "@ant-design/icons";

const people = [
  { name: "Yi-Xuan Wu", role: "Team Member" },
  { name: "Ying-Xuan He", role: "Team Member" },
  { name: "Pang-Po Cheng", role: "Team Member" },
  { name: "Chin-Yu Sun", role: "Project Advisor" },
  { name: "Sheng-Shan Chen", role: "Consultant" },
  { name: "Han-Xuan Huang", role: "Consultant" }
];

export default function About() {
  return (
    <div className="about">
      <h3 className="about-title" style={{marginTop: "0"}}><BookOutlined /> This Project</h3>
      <Card className="about-card">
        <p>The goal of this project is to develop a deep learning-based ransomware detection model and deploy it on a website, allowing users to upload and analyze files.</p>
      </Card>
      <h3 className="about-title"><TeamOutlined /> Project Advisor</h3>
      <Row gutter={16}>
        {people.filter(person => person.role === "Project Advisor").map((person, index) => (
          <Col span={8} key={index}>
            <Card className="about-card">
              <Card.Meta
                avatar={<Avatar>{person.name[0]}</Avatar>}
                title={person.name}
              />
            </Card>
          </Col>
        ))}
      </Row>
      <h3 className="about-title"><TeamOutlined /> Team Members</h3>
      <Row gutter={16}>
        {people.filter(person => person.role === "Team Member").map((person, index) => (
          <Col span={8} key={index}>
            <Card className="about-card">
              <Card.Meta
                avatar={<Avatar>{person.name[0]}</Avatar>}
                title={person.name}
              />
            </Card>
          </Col>
        ))}
      </Row>
      <h3 className="about-title"><TeamOutlined /> Consultant</h3>
      <Row gutter={16}>
        {people.filter(person => person.role === "Consultant").map((person, index) => (
          <Col span={8} key={index}>
            <Card className="about-card">
              <Card.Meta
                avatar={<Avatar>{person.name[0]}</Avatar>}
                title={person.name}
              />
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}