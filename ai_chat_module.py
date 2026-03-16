#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三角洲游戏助手 - AI问答模块（选配）
RGA检索增强AI问答实现
"""

import os
import json
from typing import List, Dict, Optional

try:
    import chromadb
    from chromadb.utils import embedding_functions
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False

class AIChatModule:
    def __init__(self, db_path: str = "./chroma_db"):
        self.db_path = db_path
        self.client = None
        self.collection = None
        self.initialized = False
        
    def is_available(self) -> bool:
        return HAS_CHROMA
        
    def initialize(self) -> bool:
        if not HAS_CHROMA:
            return False
        try:
            self.client = chromadb.PersistentClient(path=self.db_path)
            self.ef = embedding_functions.DefaultEmbeddingFunction()
            self.collection = self.client.get_or_create_collection(
                name="delta_game_knowledge",
                embedding_function=self.ef
            )
            self.initialized = True
            return True
        except Exception as e:
            print(f"AI模块初始化失败: {e}")
            return False
            
    def add_documents(self, documents: List[Dict], ids: Optional[List[str]] = None):
        if not self.initialized:
            return False
        try:
            texts = [doc["content"] for doc in documents]
            metadatas = [{"title": doc.get("title", "")} for doc in documents]
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(documents))]
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as e:
            print(f"添加文档失败: {e}")
            return False
            
    def query(self, question: str, n_results: int = 3) -> List[Dict]:
        if not self.initialized:
            return []
        try:
            results = self.collection.query(
                query_texts=[question],
                n_results=n_results
            )
            return [
                {
                    "content": doc,
                    "title": meta["title"],
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception as e:
            print(f"查询失败: {e}")
            return []
            
    def generate_answer(self, question: str, retrieved_docs: List[Dict]) -> str:
        if not retrieved_docs:
            return "抱歉，没有找到相关资料，请尝试其他问题。"
        context = "\n\n".join([f"【{doc['title']}】\n{doc['content']}" for doc in retrieved_docs])
        answer = f"根据检索到的资料，为您解答：\n\n{context}\n\n以上信息仅供参考，请结合实际游戏情况判断。"
        return answer
        
    def chat(self, question: str) -> str:
        retrieved = self.query(question)
        return self.generate_answer(question, retrieved)
        
    def load_default_knowledge(self, skills_path: str = "skills.json"):
        if not os.path.exists(skills_path):
            return False
        try:
            with open(skills_path, 'r', encoding='utf-8') as f:
                skills = json.load(f)
            docs = []
            for category in skills.values():
                for skill in category:
                    docs.append({
                        "title": skill["name"],
                        "content": f"{skill['description']}\n\n{skill['content']}"
                    })
            extra_docs = [
                {
                    "title": "游戏基本介绍",
                    "content": "三角洲游戏是一款战术射击游戏，玩家需要在地图中搜刮物资、击败敌人、安全撤离。"
                },
                {
                    "title": "修脚技巧",
                    "content": "修脚是指专门攻击敌人腿部的战术，可以快速击倒敌人而不直接击杀，适合以小搏大的战术。"
                }
            ]
            docs.extend(extra_docs)
            return self.add_documents(docs)
        except Exception as e:
            print(f"加载默认知识库失败: {e}")
            return False

def install_dependencies():
    import subprocess
    import sys
    packages = ["chromadb", "sentence-transformers"]
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"安装 {package} 失败，请手动安装")
            return False
    return True

if __name__ == "__main__":
    print("AI问答模块 - 三角洲游戏助手")
    if not HAS_CHROMA:
        print("未检测到依赖，正在安装...")
        if install_dependencies():
            print("依赖安装成功，请重启程序")
        else:
            print("依赖安装失败")
    else:
        print("依赖已就绪")
