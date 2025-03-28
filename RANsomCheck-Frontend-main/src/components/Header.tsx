import { useState, useEffect } from "react";
import { Link, Location, useLocation } from "react-router-dom";
import type { MenuProps } from "antd";
import { Menu } from "antd";
import LOGO_BLUE from "../assets/logo.png";

type MenuItem = Required<MenuProps>["items"][number];

const items: MenuItem[] = [
  {
    key: "home",
    label: <Link to="/"><img src={LOGO_BLUE} alt="Logo" style={{height: "2rem", margin: "10px 0", marginRight: "5px" }}/>RANsomCheck</Link>
  },
  {
    key: "analysis",
    label: <Link to="/analysis">Analysis</Link>
  },
  {
    key: "about",
    label: <Link to="/about">About</Link>
  }
];

function GetPath(location: Location): string {
  const pathParts = location.pathname.split("/");

  if (pathParts[1] === "") {
    return "home";
  }
  else {
    return pathParts[1];
  }
}

export default function Header() {
  const [current, setCurrent] = useState("home");
  const location = useLocation();

  useEffect(() => {
    setCurrent(GetPath(location));
  });

  return (
    <div className="header">
        <Menu selectedKeys={[current]} mode="horizontal" items={items} style={{fontSize: "1rem", fontWeight: "bold"}}/>
    </div>
  );
}