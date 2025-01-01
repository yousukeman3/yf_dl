"""yfinanceを用いた株価データの取得プログラムです。"""
import argparse
import time
import os
import yfinance as yf

def main():
    """プログラムのメイン関数です。"""

    # 引数の設定
    parser = argparse.ArgumentParser(description='yfinanceを用いた株価データの取得プログラムです。')

    parser.add_argument('dir' , help='データの保存先を指定してください。', type=str)
    parser.add_argument('-m', '--make_dir',
                        help='データの保存先が存在しない場合、ディレクトリを作成します。',
                        action='store_true')
    parser.add_argument('-n','--no_floor',help='取得したデータを切り捨てずに保存します。',action='store_true')
    parser.add_argument('brand_file' , help='取得したい株価データの銘柄コードを改行で区切ったtxtファイルを指定してください。', type=str)

    args = parser.parse_args()

    # 経過時間の計測用の変数
    start_time : float

    # 銘柄リストの読み込み
    with open(args.brand_file, 'r', encoding='utf-8') as f:

        # 銘柄リストの読み込み
        brand_list = f.readlines()

        # 銘柄ごとのデータの取得
        for brand in brand_list:

            # 開始時間の記録
            start_time = time.time()

            # 銘柄の取得
            brand = brand.strip()

            # データの取得
            print(f'銘柄:{brand}のデータの取得を開始します。')
            try:
                data = yf.download(brand+'.T')
            except BaseException as e:
                print(f'エラー:{e}')
                break

            # データの整形
            if not args.no_floor:
                data = data.astype(int).reindex(
                    columns=[('Open',brand+'.T'),
                             ('High',brand+'.T'),
                             ('Low',brand+'.T'),
                             ('Close',brand+'.T'),
                             ('Volume',brand+'.T')
                             ])
            data.columns = ['Open','High','Low','Close','Volume']

            # データの保存先の作成
            if args.make_dir:
                if not os.path.exists(args.dir):
                    os.makedirs(args.dir)

            # データの保存
            try:
                data.to_csv(os.path.join(args.dir, brand + '.csv'))
            except OSError as e:
                print(f'エラー:{e}')
                break
            print(f'銘柄:{brand}のデータの取得が完了しました。')

            # 経過時間が2秒未満の場合、2秒になるまで待機
            if (start_time - time.time()) < 2:
                time.sleep(2 - (start_time - time.time()))

# プログラムの実行
if __name__ == '__main__':
    main()
