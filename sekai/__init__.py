import aiohttp
import xml.etree.ElementTree as ET
from urllib.parse import quote
import os

class Sekai:
    def __init__(self, server:str="jp"):
        self.server: str = server

    async def listdir(self, path:str)->list[str]:
        # https://storage.sekai.best/sekai-jp-assets/?delimiter=%2F&list-type=2&max-keys=1000&prefix=comic%2Fone_frame%2F
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://storage.sekai.best/sekai-{self.server}-assets/?delimiter=%2F&list-type=2&max-keys=1000&prefix={quote(path)}") as resp:
                xml = await resp.text()
                # 解析XML响应（处理命名空间）
                root = ET.fromstring(xml)
                # 定义S3命名空间
                namespaces = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
                # 使用命名空间查找所有Key元素
                key_elements = root.findall('.//s3:Key', namespaces)
                # 提取Key文本内容并过滤空值
                paths = [elem.text for elem in key_elements if elem.text]
                return paths

    async def get(self, path:str):
        # https://storage.sekai.best/sekai-jp-assets/comic/one_frame/comic_0001.png
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://storage.sekai.best/sekai-{self.server}-assets/{path}") as resp:
                return await resp.read()

    async def download(self, path:str):
        data = await self.get(path)
        path=f"sekai-{self.server}-assets/"+path
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)

