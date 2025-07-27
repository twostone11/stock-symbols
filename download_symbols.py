import yfinance as yf
import json
import os
import time
import pandas as pd
from datetime import datetime, timedelta
import logging
import argparse

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_symbols_from_json():
    """从三个JSON文件中加载股票代码"""
    exchanges = ["nasdaq", "amex", "nyse"]
    all_symbols = []
    
    for exchange in exchanges:
        file_path = f"{exchange}.json"
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 提取股票代码
                symbols = [item.get('symbol', '') for item in data if item.get('symbol')]
                logger.info(f"从 {exchange}.json 加载了 {len(symbols)} 个股票代码")
                all_symbols.extend(symbols)
            else:
                logger.warning(f"文件 {file_path} 不存在")
        except Exception as e:
            logger.error(f"读取 {file_path} 时出错: {e}")
    
    logger.info(f"总共加载了 {len(all_symbols)} 个股票代码")
    return all_symbols

def create_stock_data_directory():
    """创建股票数据存储目录"""
    stock_data_dir = "stock_data"
    if not os.path.exists(stock_data_dir):
        os.makedirs(stock_data_dir)
        logger.info(f"创建目录: {stock_data_dir}")
    return stock_data_dir

def download_stock_data(symbol, period="1y", start_date=None, end_date=None, stock_data_dir="stock_data"):
    """下载单个股票的数据"""
    try:
        # 创建 yfinance Ticker 对象
        ticker = yf.Ticker(symbol)
        
        # 下载历史数据
        if start_date and end_date:
            hist = ticker.history(start=start_date, end=end_date)
        elif start_date:
            hist = ticker.history(start=start_date)
        else:
            hist = ticker.history(period=period)
        
        if hist.empty:
            logger.warning(f"股票 {symbol} 没有数据")
            return False
        
        # 保存到CSV文件
        file_path = os.path.join(stock_data_dir, f"{symbol}.csv")
        hist.to_csv(file_path)
        
        logger.info(f"成功下载 {symbol} 的数据，保存到 {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"下载 {symbol} 数据时出错: {e}")
        return False

def download_batch_stock_data(symbols, batch_size=50, delay=1, period="1y", start_date=None, end_date=None):
    """批量下载股票数据，考虑API限制"""
    stock_data_dir = create_stock_data_directory()
    
    total_symbols = len(symbols)
    successful_downloads = 0
    failed_downloads = 0
    
    logger.info(f"开始下载 {total_symbols} 个股票的数据")
    if start_date and end_date:
        logger.info(f"时间范围: {start_date} 到 {end_date}")
    elif start_date:
        logger.info(f"起始时间: {start_date}")
    else:
        logger.info(f"时间周期: {period}")
    logger.info(f"批次大小: {batch_size}, 延迟: {delay}秒")
    
    for i in range(0, total_symbols, batch_size):
        batch = symbols[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total_symbols + batch_size - 1) // batch_size
        
        logger.info(f"处理第 {batch_num}/{total_batches} 批次 ({len(batch)} 个股票)")
        
        for j, symbol in enumerate(batch):
            # 检查文件是否已存在
            file_path = os.path.join(stock_data_dir, f"{symbol}.csv")
            if os.path.exists(file_path):
                logger.info(f"股票 {symbol} 数据已存在，跳过下载")
                successful_downloads += 1
                continue
            
            # 下载数据
            if download_stock_data(symbol, period, start_date, end_date, stock_data_dir):
                successful_downloads += 1
            else:
                failed_downloads += 1
            
            # 在每个股票下载后添加延迟，避免触发API限制
            if j < len(batch) - 1:  # 不在批次最后一个股票后延迟
                time.sleep(delay)
        
        # 批次间延迟
        if i + batch_size < total_symbols:
            logger.info(f"批次完成，等待 {delay * 2} 秒后继续...")
            time.sleep(delay * 2)
    
    logger.info(f"下载完成！成功: {successful_downloads}, 失败: {failed_downloads}")
    return successful_downloads, failed_downloads

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='股票数据下载工具')
    
    # 股票代码参数
    parser.add_argument('-s', '--symbols', type=str, nargs='+', 
                       help='指定要下载的股票代码，多个代码用空格分隔 (例如: AAPL MSFT GOOGL)')
    
    parser.add_argument('-f', '--symbols-file', type=str,
                       help='从文件读取股票代码，每行一个代码')
    
    # 时间参数
    parser.add_argument('-p', '--period', type=str, default='1y',
                       choices=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                       help='数据周期 (默认: 1y)')
    
    parser.add_argument('--start', type=str,
                       help='起始日期 (格式: YYYY-MM-DD)')
    
    parser.add_argument('--end', type=str,
                       help='结束日期 (格式: YYYY-MM-DD)')
    
    # 下载控制参数
    parser.add_argument('-b', '--batch-size', type=int, default=20,
                       help='批次大小 (默认: 20)')
    
    parser.add_argument('-d', '--delay', type=float, default=1.0,
                       help='请求间延迟秒数 (默认: 1.0)')
    
    parser.add_argument('--sample', type=int,
                       help='下载样本数据，指定数量')
    
    # 操作模式
    parser.add_argument('--interactive', action='store_true',
                       help='交互模式')
    
    parser.add_argument('--stats', action='store_true',
                       help='显示下载统计信息')
    
    return parser.parse_args()

def validate_date(date_string):
    """验证日期格式"""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError(f"无效的日期格式: {date_string}，请使用 YYYY-MM-DD 格式")

def load_symbols_from_file(file_path):
    """从文件加载股票代码"""
    symbols = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                symbol = line.strip().upper()
                if symbol:
                    symbols.append(symbol)
        logger.info(f"从文件 {file_path} 加载了 {len(symbols)} 个股票代码")
    except Exception as e:
        logger.error(f"读取文件 {file_path} 时出错: {e}")
    return symbols

def download_sample_data(sample_size=100, period="1y", start_date=None, end_date=None):
    """下载样本数据（用于测试）"""
    symbols = load_symbols_from_json()
    
    if not symbols:
        logger.error("没有找到股票代码")
        return
    
    # 取样本
    sample_symbols = symbols[:sample_size]
    logger.info(f"下载前 {len(sample_symbols)} 个股票的样本数据")
    
    return download_batch_stock_data(sample_symbols, batch_size=10, delay=0.5, 
                                   period=period, start_date=start_date, end_date=end_date)

def get_download_statistics():
    """获取下载统计信息"""
    stock_data_dir = "stock_data"
    if not os.path.exists(stock_data_dir):
        logger.info("股票数据目录不存在")
        return
    
    csv_files = [f for f in os.listdir(stock_data_dir) if f.endswith('.csv')]
    logger.info(f"已下载的股票数据文件数量: {len(csv_files)}")
    
    # 计算总文件大小
    total_size = 0
    for file in csv_files:
        file_path = os.path.join(stock_data_dir, file)
        total_size += os.path.getsize(file_path)
    
    total_size_mb = total_size / (1024 * 1024)
    logger.info(f"总数据大小: {total_size_mb:.2f} MB")

def interactive_mode():
    """交互模式"""
    print("股票数据下载工具")
    print("=" * 50)
    
    # 显示选项
    print("请选择操作:")
    print("1. 下载样本数据 (前100个股票)")
    print("2. 下载所有股票数据")
    print("3. 查看下载统计")
    print("4. 退出")
    
    choice = input("请输入选择 (1-4): ").strip()
    
    if choice == "1":
        print("开始下载样本数据...")
        download_sample_data(sample_size=100, period="1y")
        get_download_statistics()
        
    elif choice == "2":
        print("警告：下载所有股票数据可能需要很长时间！")
        confirm = input("确认继续？(y/N): ").strip().lower()
        if confirm == 'y':
            symbols = load_symbols_from_json()
            if symbols:
                download_batch_stock_data(symbols, batch_size=20, delay=1, period="1y")
                get_download_statistics()
        else:
            print("操作已取消")
            
    elif choice == "3":
        get_download_statistics()
        
    elif choice == "4":
        print("退出程序")
        
    else:
        print("无效选择")

def main():
    """主函数"""
    args = parse_arguments()
    
    # 如果只是查看统计信息
    if args.stats:
        get_download_statistics()
        return
    
    # 如果是交互模式
    if args.interactive:
        interactive_mode()
        return
    
    # 验证日期格式
    start_date = None
    end_date = None
    if args.start:
        start_date = validate_date(args.start)
    if args.end:
        end_date = validate_date(args.end)
    
    # 获取股票代码
    symbols = []
    if args.symbols:
        symbols = [s.upper() for s in args.symbols]
        logger.info(f"使用命令行指定的 {len(symbols)} 个股票代码")
    elif args.symbols_file:
        symbols = load_symbols_from_file(args.symbols_file)
    elif args.sample:
        symbols = load_symbols_from_json()[:args.sample]
        logger.info(f"使用样本数据，前 {len(symbols)} 个股票代码")
    else:
        symbols = load_symbols_from_json()
        logger.info(f"使用所有股票代码，共 {len(symbols)} 个")
    
    if not symbols:
        logger.error("没有找到要下载的股票代码")
        return
    
    # 开始下载
    logger.info(f"准备下载 {len(symbols)} 个股票的数据")
    download_batch_stock_data(
        symbols=symbols,
        batch_size=args.batch_size,
        delay=args.delay,
        period=args.period,
        start_date=start_date,
        end_date=end_date
    )
    
    # 显示统计信息
    get_download_statistics()

if __name__ == "__main__":
    main()