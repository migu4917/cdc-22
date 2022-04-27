import { Alert } from "antd";
import { useEffect } from "react";
import KashHeader from "../../components/Header";

export default function Home() {
    return (
        <>
            <KashHeader />
            <Alert message="请点击上述功能按钮开始使用" type="info" showIcon closable
                description="请点击上述功能按钮开始使用"/>
        </>
    )
}