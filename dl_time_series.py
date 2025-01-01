"""yfinanceを用いた株価データの取得プログラムです。"""
import argparse
import time
import os
import yfinance as yf

def main():
    """プログラムのメイン関数です。"""
    parser = argparse.ArgumentParser(description='yfinanceを用いた株価データの取得プログラムです。')

    parser.add_argument('dir' , help='データの保存先を指定してください。', type=str)
    parser.add_argument('-m', '--make_dir',
                        help='データの保存先が存在しない場合、ディレクトリを作成します。',
                        action='store_true')
    parser.add_argument('brand_file' , help='取得したい株価データの銘柄コードを改行で区切ったtxtファイルを指定してください。', type=str)

    args = parser.parse_args()
    start_time : float

    with open(args.brand_file, 'r', encoding='utf-8') as f:
        brand_list = f.readlines()
        for brand in brand_list:
            start_time = time.time()
            brand = brand.strip()
            print(f'銘柄:{brand}のデータの取得を開始します。')
            try:
                data = yf.download(brand+'.T')
            except BaseException as e:
                print(f'エラー:{e}')
                break
            if args.make_dir:
                if not os.path.exists(args.dir):
                    os.makedirs(args.dir)
            try:
                data.to_csv(os.path.join(args.dir, brand + '.csv'))
            except OSError as e:
                print(f'エラー:{e}')
                break
            print(f'銘柄:{brand}のデータの取得が完了しました。')
            if (start_time - time.time()) < 2:
                time.sleep(2 - (start_time - time.time()))


if __name__ == '__main__':
    main()
