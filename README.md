AyakashiProxy
=======================

\--------------------------------------------
A tool for playing Ayakashi Ghost Guild in your web browser
---------------------

\--------------------------------------------
更新见：https://github.com/jackyzy823/AyakashiProxy
---------------------


使用说明

压缩包内容:
Ayakashi.exe ---主程序
library.zip  ---运行库
settings.ini ---配置文件
readme.txt   ---本文件

下载压缩包，解压，打开ayakashiproxy.exe

1.知道自己的USERKEY
直接在输入框内输入USERKEY后点击确定，启动HTTP代理。
浏览器端设置：
    1)Chrome里用SwitchySharp添加代理条目 Ayakashi 手动设置 127.0.0.1:你设置的端口号或者默认的12345 添加规则 *://zc2.ayakashi.zynga.com/* 走Ayakashi代理
    

2.不知带自己的USERKEY
第一次操作
点击监听，然后让手机和电脑在同一个无线内，
IPHONE手机在设置->无线局域网->当前连接的无线 点击右边的感叹号->HTTP代理 -填入你电脑的IP-端口填你设置的端口号或者默认的12345-返回-打开灵异阴阳录，程序会自动抓取流量找出USERKEY，然后自动开启代理
Android手机设置类似 设置-WiFi-长按当前连接的无线-修改网络-显示高级选项-代理设置-手动- 填入你电脑的IP  然后端口填你设置的端口号或者默认的12345- 返回-打开灵异阴阳录

!监听完后请一定要将以上手机端的设置还原。

监听完后USERKEY写入settings.ini，下次打开程序时，就会自动出现在输入框内，点击确认就可。
浏览器端设置与1相同

3.在浏览器输入 http://zc2.ayakashi.zynga.com/app.php?_c=entry&action=mypage 进入首页

按钮的替代连接

初始页面 
http://zc2.ayakashi.zynga.com/app.php?_c=entry&action=initialize

首页 
http://zc2.ayakashi.zynga.com/app.php?_c=entry&action=mypage

登陆奖励
http://zc2.ayakashi.zynga.com/app.php?day=3&_c=login_bonus&action=seven_days

封印石
http://zc2.ayakashi.zynga.com/app.php?_c=parts&action=default

式神一览
http://zc2.ayakashi.zynga.com/app.php?_c=monster&action=list

名鉴
http://zc2.ayakashi.zynga.com/app.php?_c=album&action=default

商店
http://zc2.ayakashi.zynga.com/app.php?_c=item&action=default&tab=tab-shop-list 

新消息
http://zc2.ayakashi.zynga.com/app.php?_c=information&action=default

设定
http://zc2.ayakashi.zynga.com/app.php?_c=settings&action=default

同伴
http://zc2.ayakashi.zynga.com/app.php?_c=friend&action=default

交换铺
http://zc2.ayakashi.zynga.com/app.php?_c=gacha&action=exchangeList

收件箱
http://zc2.ayakashi.zynga.com/app.php?_c=webMessageCenter&action=default







端口号设置:
第一次运行后在程序目录下生成settings.ini,或者可能打包时已自带了
如果默认端口12345被别的程序占用了，修改文件中PORT的值 1024~65535之间 
修改后相应的代理(Chrome中的SwitchySharp或者IE的全局代理等)设置也要修改

-----------------------
TODO:
1.增加最小化到托盘
2.处理图标问题
3.完善说明
4.增加新建账号功能
----------------------
可能考虑完成：
1.自动练级刷图等功能


