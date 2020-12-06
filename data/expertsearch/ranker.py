import math
import sys
import time
import metapy
import pytoml

class KLDivergenceRanker(metapy.index.RankingFunction):
    def __init__(self, cfg_file):
        self.forward_idx = metapy.index.make_forward_index(cfg_file)
        self.ranker = metapy.index.JelinekMercer(0.667)
        super(KLDivergenceRanker, self).__init__()

    def score(self, idx, query, nd):
        ql = len(query.content().split())

        k = max(50 - 3 * ql, 3)
        k = min(k, 50)

        kl = metapy.index.KLDivergencePRF(self.forward_idx, self.ranker, 0.78239, 0.64786911, int(k))
        return kl.score(idx, query, nd)

def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate, 
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    try:
        return KLDivergenceRanker(cfg_file)
    except:
        return metapy.index.OkapiBM25(k1=2.2, b=0.72, k3=500) # 0.9332

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    ndcg = 0.0
    num_queries = 0

    print('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            ndcg += ev.ndcg(results, query_start + query_num, top_k)
            num_queries+=1
    ndcg= ndcg / num_queries
            
    print("NDCG@{}: {}".format(top_k, ndcg))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
