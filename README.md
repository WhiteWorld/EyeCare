# Eye Care 应用打包指南

## 依赖安装

在打包前请确保已安装以下依赖：

```bash
pip install rumps py2app
```

## 打包步骤

1. 确保当前目录为项目根目录
2. 运行以下命令进行打包：

```bash
python setup.py py2app
```

3. 打包完成后，应用会生成在 `dist` 目录下

## 常见问题

### 图标不显示
确保 `app_icon.icns` 文件存在于项目根目录

### 打包失败
检查是否已安装所有依赖，特别是 `rumps` 和 `py2app`

## 运行应用

打包完成后，可直接双击 `dist/Eye Care.app` 运行应用