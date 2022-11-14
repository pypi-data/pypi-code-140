# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_apex_api_query']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'nonebot2>=2.0.0rc1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-apex-api-query',
    'version': '22.11.15',
    'description': '基于 NoneBot2 的 Apex Legends API 查询插件',
    'long_description': '# Apex API Query\nApex Legends API 查询插件\n\n## 使用方法\n在 `nonebot-plugin-apex-api-query.py` 中的第 10 行填入您的 API 密钥。\n您可以点击 [此处](https://portal.apexlegendsapi.com/) 申请 API 密钥。\n在 Bot 私聊 或 已加入的群聊 中发送命令。\n\n### 查询玩家信息\n`/bridge [玩家名称]` 、 `/玩家 [玩家名称]`\n暂不支持 UID 查询。\n\n输出示例：\n```text\n玩家信息: \n名称: HxiaoH \nUID: 1002727553409 \n平台: PC \n等级: 215 \n封禁状态: 否 \n剩余秒数: 0 \n最后封禁原因: 竞技逃跑冷却\n大逃杀段位: 黄金 4 \n大逃杀分数: 5828 \n竞技场段位: 白银 3 \n竞技场分数: 2317 \n大厅状态: 打开 \n在线: 否 \n游戏中: 否 \n可加入: 否 \n群满员: 否 \n已选传奇: 地平线 \n当前状态: 离线 \n当前状态时长: 15:08:37 \n```\n\n### 查询大逃杀地图轮换\n`/maprotation` 、 `/地图`\n\n输出示例：\n```text\n大逃杀: \n当前地图: 奥林匹斯 \n下个地图: 世界尽头 \n剩余时间: 00:06:27 \n```\n\n### 查询猎杀者信息\n`/predator` 、 `/猎杀`\n\n输出示例：\n```text\n大逃杀: \nPC 端: \n猎杀者人数: 750 \n猎杀者分数: 15551 \n大师和猎杀者人数: 1077 \nPS4/5 端: \n猎杀者人数: -1 \n猎杀者分数: 15000 \n大师和猎杀者人数: 484 \nXbox 端: \n猎杀者人数: -1 \n猎杀者分数: 15000 \n大师和猎杀者人数: 232 \nSwitch 端: \n猎杀者人数: -1 \n猎杀者分数: 15000 \n大师和猎杀者人数: 16 \n竞技场: \nPC 端: \n猎杀者人数: 750 \n猎杀者分数: 8063 \n大师和猎杀者人数: 971 \nPS4/5 端: \n猎杀者人数: 742 \n猎杀者分数: 8291 \n大师和猎杀者人数: 1812 \nXbox 端: \n猎杀者人数: -1 \n猎杀者分数: 8000 \n大师和猎杀者人数: 648 \nSwitch 端: \n猎杀者人数: -1 \n猎杀者分数: 8000 \n大师和猎杀者人数: 96 \n```\n\n### 查询复制器轮换\n`/crafting` 、 `/制造`\n\n输出示例：\n```text\n每日制造: \n加长式重型弹匣 等级3 35 点 \n铁砧接收器 等级4 45 点\n每周制造: \n击倒护盾 等级3 30 点\n移动重生信标 等级2 50 点\n赛季制造: \n和平捍卫者 等级1 30 点\n喷火轻机枪 等级1 30 点\n```',
    'author': 'HxiaoH',
    'author_email': '412454922@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/H-xiaoH/nonebot-plugin-apex-api-query',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
