class GeneVocabulary:
    D_GENEID = {}
    D_GENSYMBOL = {}

    def __init__(self,  gene_vocabulary_path):
        with open(gene_vocabulary_path) as in_f:
            for line in in_f:
                if line.startswith('#'):
                    continue
                sp_line = line.strip('\n').split('\t')

                gene_symbol = sp_line[0]
                gene_name = sp_line[1]
                gene_id = "GENEID:" + sp_line[2]

                self.D_GENEID[gene_id] = gene_symbol
                self.D_GENSYMBOL[gene_symbol] = gene_id
