# 2. pip包管理

## pip是什么

pip是Python的包管理器，类比Java的Maven/Gradle。从PyPI（Python Package Index）下载安装包。

## 常用命令速查

| 命令 | 说明 |
|------|------|
| `pip install 包名` | 安装包 |
| `pip install 包名==1.0.0` | 安装指定版本 |
| `pip install 包名>=1.0.0` | 安装最低版本 |
| `pip install -U 包名` | 升级包 |
| `pip uninstall 包名` | 卸载包 |
| `pip list` | 列出已安装的包 |
| `pip show 包名` | 查看包详情 |
| `pip freeze` | 输出所有包及版本 |
| `pip install -r requirements.txt` | 从文件安装 |
| `pip freeze > requirements.txt` | 导出依赖 |

## 版本指定

| 写法 | 含义 |
|------|------|
| `==1.0.0` | 精确版本 |
| `>=1.0.0` | 最低版本 |
| `<=2.0.0` | 最高版本 |
| `>=1.0.0,<2.0.0` | 版本范围 |
| `~=1.0.0` | 兼容版本（1.0.x） |

## 镜像源配置（国内必配）

PyPI默认服务器在国外，国内下载慢。配置国内镜像：

### 临时使用
```bash
pip install requests -i https://mirrors.aliyun.com/pypi/simple/
```

### 永久配置
```bash
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

### 常用镜像

| 镜像 | 地址 |
|------|------|
| 阿里云 | `https://mirrors.aliyun.com/pypi/simple/` |
| 清华 | `https://pypi.tuna.tsinghua.edu.cn/simple/` |
| 豆瓣 | `https://pypi.doubanio.com/simple/` |
| 中科大 | `https://pypi.mirrors.ustc.edu.cn/simple/` |

## 升级pip自身

```bash
python -m pip install --upgrade pip
```

## 常见问题

| 问题 | 解决 |
|------|------|
| 安装慢 | 配置国内镜像 |
| 权限错误 | 用虚拟环境，不要sudo pip |
| 版本冲突 | 用虚拟环境隔离 |
| 找不到包 | 检查包名拼写，去pypi.org搜 |
