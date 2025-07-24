@echo off

REM 创建虚拟环境设置脚本 (适用于 Windows)

echo 正在创建虚拟环境...
python -m venv venv

echo 正在激活虚拟环境...
call venv\Scripts\activate.bat

echo 正在安装依赖包...
pip install -r requirements.txt

echo 虚拟环境设置完成！
echo 要激活虚拟环境，请运行: venv\Scripts\activate.bat
echo 要退出虚拟环境，请运行: deactivate

pause