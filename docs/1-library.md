# Library
このセクションでは主要なライブラリについて解説します。



## Asyncio
並列処理とは、複数の計算を同時に実行することを指します。これにより、計算速度を向上させたり、複数のタスクを同時に処理することが可能になります。

Pythonでは、ほかにも以下の方法で並列処理を実現できます：
- `threading.Thread`: スレッドを使用して並列処理を行います。軽量で、同一プロセス内で複数のスレッドが実行されますが、グローバルインタプリタロック（GIL）の影響を受けるため、CPUバウンドのタスクには適していません。
- `multiprocessing.Process`: プロセスを使用して並列処理を行います。各プロセスは独立したメモリ空間を持つため、GILの影響を受けず、CPUバウンドのタスクに適しています。
- `concurrent.futures`: 高レベルのインターフェースを提供し、スレッドまたはプロセスプールを使用して並列処理を簡単に実装できます。
- `asyncio`: 非同期I/O操作を効率的に処理するためのライブラリで、シングルスレッド内での並行処理を実現します。

これらの方法を使用することで、Pythonで効率的な並列処理を実現することができます。

### Asyncioの基本的な考え方

`asyncio` は、Pythonで非同期I/O操作を効率的に処理するためのライブラリです。`asyncio` を使用することで、シングルスレッド内での並行処理を実現できます。

#### コルーチン
シングルスレッド内で並列処理を実現するためにはコルーチンという概念を理解する必要があります。

コルーチン
- シングルスレッド: コルーチンはシングルスレッド内で実行され、イベントループによって管理されます。
- 非同期I/Oに最適: コルーチンはI/Oバウンドのタスク（ネットワーク操作やファイル操作など）に最適です。
- 軽量: スレッドに比べて軽量で、コンテキストスイッチのオーバーヘッドが少ないです。
- 協調的マルチタスク: コルーチンは明示的にawaitを使用して他のタスクに制御を渡します。

マルチスレッド
- マルチスレッド: マルチスレッドは複数のスレッドを使用して並列にタスクを実行します。
- CPUバウンドのタスクに適: マルチスレッドはCPUバウンドのタスク（計算集約型の処理など）に適しています。
- 重い: スレッドはコルーチンに比べて重く、コンテキストスイッチのオーバーヘッドが大きいです。
- プリエンプティブマルチタスク: スレッドはOSによってスケジューリングされ、明示的に制御を渡す必要はありません。

# コルーチンの実装
コルーチンは、asyncio の非同期タスクの基本単位です。コルーチンは、async def キーワードを使用して定義され、await キーワードを使用して他のコルーチンや非同期操作を待機することができます。

コルーチンの基本的な使い方は以下の通りです：


```python
import asyncio

async def say_hello():
    print('Hello')
    await asyncio.sleep(1)
    print('World')

# コルーチンをイベントループで実行
asyncio.run(say_hello())
```
この例では、say_hello コルーチンが定義され、await asyncio.sleep(1) によって1秒間待機します。この間、イベントループは他のタスクを実行することができます。

つぎにコルーチンを用いて並列処理を実行してみます。
```python
import asyncio

async def func1():
    print('func1() started')
    await asyncio.sleep(1)
    print('func1() finished')

async def func2():
    print('func2() started')
    await asyncio.sleep(1)
    print('func2() finished')

async def main():
    task1 = asyncio.create_task(func1())
    task2 = asyncio.create_task(func2())
    await task1
    await task2

asyncio.run(main())
```
実行してみると約1秒で処理が終了します。
このようにfunc1, func2をコルーチンとして包み、並列処理を行っています。
そして ``` task = asyncio.create_task()```を呼び出すことで、コルーチンオブジェクトを生成し```await task ```を呼び出すことで、コルーチンを実行します。

awaitの目的は、処理が終了するまで、ほかのタスク（コルーチン）に実行権利（制御権利）を移す、ということです。この場合、```await asyncio.sleep(1)```で1秒処理を止める、ということを明示的に記述しています。言い換えればこれは1秒間ほかのコルーチンにスレッドの制御を譲るということを意味します。
ファイルからデータを読み込む処理を```await readLine()```とします。この場合、ディスクからファイルのデータを読み込むためI/O blockingが発生します。コルーチンでは、このI/O blocking中にほかのコルーチンにスレッドの制御権利を移します。

```await asyncio.sleep(1)```に戻りましょう。似たような関数として`time.sleep(1)`があります。これも一秒間処理を停止する処理ですがコルーチン用ではありません。したがってほかのコルーチンに制御権利を渡しません。

まとめ。`await/async`で制御権利をコントロールすることが大切です。


## マルチスレッド処理

さて、コルーチンは並列処理に利用できます。ですが、所詮一つのスレッドをコルーチン間で共有して使っています。

したがって、ほかのコルーチンに制御権利を譲渡しない以下のようなプログラムを実行してみます。
実行完了までは2秒かかると思います。

```python
import asyncio
import concurrent.futures
import time

async def func1():
    print("func1() started")
    time.sleep(1)
    print("func1() finished")

async def func2():
    print("func2() started")
    time.sleep(1)
    print("func2() finished")

async def main():
    task1 = asyncio.create_task(func1())
    task2 = asyncio.create_task(func2())
    await task1
    await task2

asyncio.run(main())
```

Asyncioではコルーチンではなくマルチスレッド処理も可能です。
スレッドプールから利用可能なスレッドを取得し、実行することができます。

```python
import asyncio
import concurrent.futures
import time

def func1():
    print("func1() started")
    time.sleep(1)
    print("func1() finished")

def func2():
    print("func2() started")
    time.sleep(1)
    print("func2() finished")

async def main():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        task1 = loop.run_in_executor(pool, func1)
        task2 = loop.run_in_executor(pool, func2)
        await task1
        await task2

asyncio.run(main())
```


## Future
他のコルーチンの処理結果を待つことができます。
また、値を取得することができます。

```python
import asyncio

async def get_http_response(future):
    print("Get http response")
    await asyncio.sleep(2)  # Simulate an asynchronous operation
    future.set_result("Hello http!")  # Set the result of the future

async def main():
    # Futureオブジェクトを作成
    future = asyncio.Future()

    # サーバからテキストを取得するコルーチンを起動
    asyncio.create_task(get_http_response(future))

    print("Waiting for the future result...")
    
    # future.set_result("Hello http!")が呼び出されるまで待つ
    result = await future
    print("result:", result)

asyncio.run(main())
```



# 参考文献
- https://docs.python.org/ja/3/library/asyncio-eventloop.html
- https://docs.python.org/3/library/asyncio.html
- https://qiita.com/everylittle/items/57da997d9e0507050085

