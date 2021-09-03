# smart_remote_control

https://qiita.com/takjg/items/e6b8af53421be54b62c9

### pigpioのインストール
```
sudo apt update && sudo apt upgrade -y
sudo apt install pigpio python3-pigpio
sudo systemctl enable pigpiod.service    # ラズパイ再起動時に pigpiod を自動的に起動させます
sudo systemctl start pigpiod             # いますぐ pigpiod を起動
```

### GPIOの設定
GPIO17を、output（w）に設定し、出力を low（0）にしておきます。
GPIO18を、input（r）、かつ、pull up（u）に設定します。
（注意：設定内容は電子回路によって異なります。市販の既製品などを制御する場合は、製品に応じた設定が必要です。）

```
echo 'm 17 w   w 17 0   m 18 r   pud 18 u' > /dev/pigpio
```

さらに、ラズパイの起動時に、自動的にGPIOの設定を行うようにします。
（先ほど同様、電子回路に応じた内容で設定してください。）

```
crontab -e
# 初めての場合は、どのエディタで編集するか聞かれるので、好きなエディタを選んでください。
# 最後の行に以下の1行を追加して保存。
@reboot until echo 'm 17 w   w 17 0   m 18 r   pud 18 u' > /dev/pigpio; do sleep 1s; done
```

（ちなみに、これは「デーモンpigpiodが起動して、GPIOの設定が成功するまで、1秒おきに設定を試みる」という設定です。）

### 学習
例えば、照明をONにする赤外線コードを学習するには、以下のコマンドを実行してから、リモコンのONボタンを押します。

```
python3 irrp.py -r -g18 -f codes light:on --no-confirm --post 130
Recording
Press key for 'light:on'
Okay
```
学習した赤外線コードは、-fで指定したファイル codes に、light:on という名前で記録されます。-r は record、-g18はGPIO18という意味です。--no-confirmを指定しない場合は、確認用にもう一度、リモコンの同じボタンを押すように促されます。また、--post 130には、学習を打ち切る目安を指定します。この場合、赤外線の受信が130ミリ秒途絶えたら、そこで赤外線コードが終了したものとみなされます。
