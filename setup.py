import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-plugin-hx-yinying",
    version="0.0.1",
    author="Huan Xin",
    author_email="mc.xiaolang@foxmail.com",
    description="chat with yinying",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huanxin996/nonebot_plugin_hx-yinying",
    packages=setuptools.find_packages(),
    install_requires=['nonebot2>=2.2.1', 'ujson>=5.9.0', 'httpx>=0.27.0', 'nonebot-adapter-onebot>=2.4.3', 'nonebot_plugin_localstore>=0.6.0', 'pydantic>=1.10.12'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)