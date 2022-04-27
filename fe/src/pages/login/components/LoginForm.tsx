import { Form, Input, Button, Checkbox, message, Alert } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useRouter } from 'next/router';

const NormalLoginForm = (props) => {
    const router = useRouter();
    const onFinish = values => {
        fetch("./user.json", {
            method: "GET",
        }).then(e => e.json())
            .then(e => {
                let loginFlag = false;
                e.data.forEach((value) => {
                    if (value.name && value.name == values.name &&
                        value.password && value.password == values.password) {
                        loginFlag = true;
                        router.push("/home")
                    }
                })
                if (!loginFlag) {
                    message.error("请输入正确的账号密码");
                }
            })
    };

    return (
        <>
            <strong
                style={{
                    width: 300,
                    top: "25%",
                    fontSize: 30,
                    position: "absolute",
                    textAlign: "center"
                }}>面向流行病学调查的可视化分析系统
            </strong>
            <Form
                style={{
                    width: 300,
                    top: "35%",
                    position: "absolute"
                }}
                name="normal_login"
                className="login-form"
                initialValues={{ remember: true }}
                onFinish={onFinish}
            >
                <Form.Item
                    name="name"
                    rules={[{ required: true, message: '请输入用户名!' }]}
                >
                    <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="用户名" />
                </Form.Item>
                <Form.Item
                    name="password"
                    rules={[{ required: true, message: '请输入密码!' }]}>
                    <Input
                        prefix={<LockOutlined className="site-form-item-icon" />}
                        type="password"
                        placeholder="密码"
                    />
                </Form.Item>
                <Form.Item>
                    <Form.Item name="remember" valuePropName="checked" noStyle>
                        <Checkbox>记住我</Checkbox>
                    </Form.Item>
                    <a style={{ position: "absolute", right: 50 }} className="login-form-forgot" href="">
                        忘记密码
                    </a>
                    <a style={{ position: "absolute", right: 0 }} href="">注册</a>
                </Form.Item>
                <Form.Item>
                    <Button style={{ width: "100%" }} type="primary" htmlType="submit" className="login-form-button">
                        登录
                    </Button>
                </Form.Item>
            </Form>
        </>
    );
};

export default NormalLoginForm;