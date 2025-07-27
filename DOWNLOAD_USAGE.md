# 股票数据下载脚本使用说明

## 功能概述

`download_symbols.py` 是一个功能强大的股票数据下载工具，支持从 yfinance API 下载股票历史数据。

## 主要特性

- 支持命令行参数控制
- 可指定特定股票代码或从文件读取
- 支持自定义时间周期和日期范围
- 批量下载控制和API限制处理
- 交互模式和统计功能

## 使用方法

### 1. 基本用法

```bash
# 查看帮助信息
python download_symbols.py --help

# 下载特定股票（使用默认1年周期）
python download_symbols.py -s AAPL MSFT GOOGL

# 下载样本数据（前100个股票）
python download_symbols.py --sample 100
```

### 2. 时间控制参数

```bash
# 指定数据周期
python download_symbols.py -s AAPL -p 6mo  # 6个月数据
python download_symbols.py -s AAPL -p 2y   # 2年数据

# 指定具体日期范围
python download_symbols.py -s AAPL --start 2024-01-01 --end 2024-06-30

# 只指定起始日期（到当前日期）
python download_symbols.py -s AAPL --start 2024-01-01
```

### 3. 股票代码来源

```bash
# 命令行指定多个股票
python download_symbols.py -s AAPL MSFT GOOGL TSLA AMZN

# 从文件读取股票代码
python download_symbols.py -f symbols.txt

# 使用JSON文件中的样本数据
python download_symbols.py --sample 50
```

### 4. 下载控制参数

```bash
# 设置批次大小和延迟（避免API限制）
python download_symbols.py -s AAPL MSFT -b 5 -d 2.0

# 批次大小：每批下载5个股票
# 延迟：每个请求间隔2秒
```

### 5. 操作模式

```bash
# 交互模式
python download_symbols.py --interactive

# 查看下载统计
python download_symbols.py --stats
```

## 参数说明

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--symbols` | `-s` | 指定股票代码 | `-s AAPL MSFT` |
| `--symbols-file` | `-f` | 从文件读取股票代码 | `-f symbols.txt` |
| `--period` | `-p` | 数据周期 | `-p 1y` |
| `--start` | | 起始日期 | `--start 2024-01-01` |
| `--end` | | 结束日期 | `--end 2024-12-31` |
| `--batch-size` | `-b` | 批次大小 | `-b 10` |
| `--delay` | `-d` | 延迟秒数 | `-d 1.5` |
| `--sample` | | 样本数量 | `--sample 100` |
| `--interactive` | | 交互模式 | |
| `--stats` | | 显示统计 | |

## 支持的时间周期

- `1d`, `5d` - 短期数据
- `1mo`, `3mo`, `6mo` - 月度数据  
- `1y`, `2y`, `5y`, `10y` - 年度数据
- `ytd` - 年初至今
- `max` - 最大可用数据

## 股票代码文件格式

创建一个文本文件，每行一个股票代码：

```
AAPL
MSFT
GOOGL
TSLA
AMZN
```

## 输出

- 数据保存在 `stock_data/` 目录下
- 每个股票一个CSV文件，文件名为 `{股票代码}.csv`
- CSV文件包含：Date, Open, High, Low, Close, Volume 等列

## 注意事项

1. **API限制**：yfinance有请求频率限制，建议：
   - 增加延迟时间（`-d 2` 或更高）
   - 减小批次大小（`-b 10` 或更小）
   - 避免频繁请求

2. **网络问题**：如遇到网络错误，可以：
   - 重新运行脚本（已下载的文件会被跳过）
   - 增加延迟时间
   - 检查网络连接

3. **数据存储**：
   - 已存在的文件会被跳过，不会重复下载
   - 使用 `--stats` 查看已下载的数据统计

## 示例场景

### 场景1：下载特定股票的年度数据
```bash
python download_symbols.py -s AAPL MSFT GOOGL -p 1y -d 2
```

### 场景2：下载指定时间范围的数据
```bash
python download_symbols.py -s TSLA --start 2023-01-01 --end 2023-12-31 -d 1.5
```

### 场景3：批量下载文件中的股票
```bash
python download_symbols.py -f my_stocks.txt -p 6mo -b 5 -d 2
```

### 场景4：下载样本数据进行测试
```bash
python download_symbols.py --sample 20 -p 3mo -d 1
```