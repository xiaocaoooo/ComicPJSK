from sekai import Sekai
import asyncio
import os

async def main():
    print("""ComicPJSK:
日服: jp
繁体字服: tc
英文服(全球服): en
韩文服: kr
简体中文: cn""")
    server = input("Please enter server name / 请输入服名(两位字母): ")
    sekai = Sekai(server)
    paths = await sekai.listdir("comic/one_frame/")
    await asyncio.gather(*[sekai.download(path) for path in paths])
    print(f"Download completed / 下载完成 ({len(paths)})")
    os.system("pause")

if __name__ == "__main__":
    asyncio.run(main())

