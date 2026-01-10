# 摄像头设置指南

## 问题: OpenCV无法访问摄像头

### 错误信息:
```
OpenCV: not authorized to capture video (status 0), requesting...
OpenCV: camera failed to properly initialize!
```

## 解决方案

### 方法1: 系统设置授权 (推荐)

1. **打开系统设置**:
   ```bash
   open "x-apple.systempreferences:com.apple.preference.security?Privacy_Camera"
   ```

2. **在"隐私与安全性" → "摄像头"中**:
   - 找到 **Terminal** (或你使用的终端应用)
   - ✅ **勾选启用**

3. **重启终端**:
   - 关闭所有终端窗口
   - 重新打开终端

4. **运行演示**:
   ```bash
   cd "/Users/bzhang/Downloads/Advanced HCI"
   ./run_demo.sh
   ```

---

### 方法2: 使用无摄像头版本 (立即可用)

如果你不想设置权限,可以使用模拟版本:

```bash
cd "/Users/bzhang/Downloads/Advanced HCI"
./run_demo_no_camera.sh
```

这个版本:
- ✅ 不需要摄像头权限
- ✅ 使用模拟的人脸视频
- ✅ 展示所有相同的功能
- ✅ 完美用于演示

---

## 检查摄像头

### 查看可用摄像头:
```bash
system_profiler SPCameraDataType
```

你的Mac有以下摄像头:
- FaceTime高清相机 (内置)
- OBS Virtual Camera
- "Bowen"的相机

### 测试摄像头访问:
```bash
source venv/bin/activate
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK:', cap.isOpened()); cap.release()"
```

---

## 两个版本对比

| 特性 | 真实摄像头版本 | 模拟版本 |
|------|---------------|---------|
| 需要权限 | ✅ 需要 | ❌ 不需要 |
| 真实人脸 | ✅ 是 | ❌ 模拟 |
| 情绪检测 | 模拟 | 模拟 |
| 所有UI功能 | ✅ | ✅ |
| 语音命令 | ✅ | ✅ |
| 演示效果 | 更真实 | 同样好 |

**注意**: 两个版本的情绪检测都是模拟的(因为TensorFlow不兼容Python 3.14),但UI和交互完全相同。

---

## 推荐使用

### 用于演示/答辩:
👉 **使用模拟版本** (`demo_no_camera.py`)
- 不需要设置
- 更可靠
- 效果相同

### 用于测试真实摄像头:
👉 **使用真实版本** (`demo_mode.py`)
- 授权后使用
- 显示真实视频
- 更有说服力

---

## 快速启动命令

### 模拟版本 (推荐):
```bash
./run_demo_no_camera.sh
```

### 真实摄像头版本:
```bash
./run_demo.sh
```
