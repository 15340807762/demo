import os
import logging
import time
import torch 
import torch_npu 
from torch_npu.contrib import transfer_to_npu
logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

# 写入库

from haystack.document_stores import FAISSDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline

# 创建库以及索引
document_store = FAISSDocumentStore(faiss_index_factory_str="Flat", embedding_dim=768)

# 加载已有的document_store
# document_store = FAISSDocumentStore.load(index_path="wiki_faiss_index.faiss", config_path="wiki_faiss_index.json")

doc_dir = '/dev/shm/dbc/haystack-1.x/datasets'

# 对文档进行预处理
files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(file_paths=files_to_index)

# 查看切分后的文档
# print(document_store.get_all_documents())

from haystack.nodes import EmbeddingRetriever

# 对文档进行中文相似度embedding，并更新faiss库
retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="/dev/shm/dbc/haystack-1.x/model/shi",
)

document_store.update_embeddings(retriever)
# 将faiss库索引进行持久化存储
document_store.save(index_path="wiki_faiss_index.faiss")

# 使用中文的QA模型进行问答，对检索出的结果和用户输入的问题，生成回答，该回答基本是言简意赅，这个部分可以替换为大模型解析
from haystack.nodes import FARMReader

reader = FARMReader(model_name_or_path="/dev/shm/dbc/haystack-1.x/model/qa", use_gpu=True, context_window_size=300,
                    max_seq_len=512)

from haystack.utils import print_answers
from haystack.pipelines import ExtractiveQAPipeline

# 将检索器，阅读器插入进抽取式问答管道。
pipe = ExtractiveQAPipeline(reader, retriever)

# 提问
while True:
    q = input('输入问题吧：')
    st_time = time.time()
    prediction = pipe.run(
        query=q,
        params={
            "Retriever": {"top_k": 5},
            "Reader": {"top_k": 1}
        }
    )
    # 打印结果
    # print(prediction)
    print_answers(prediction, details="all")
    end_time = time.time()

    print("计算时间为：{}".format(end_time - st_time))
